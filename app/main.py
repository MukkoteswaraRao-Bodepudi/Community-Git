import logging, shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, HTTPException
from app.database import initialize, save_candidate, get_candidate, save_job, save_match, list_rows
from app.models import Job
from resumes.parser import parse_resume
from matching.engine import match
logging.basicConfig(level=logging.INFO)
app=FastAPI(title='Generative AI Job Pipeline',version='1.0.0')
@app.on_event('startup')
def startup(): initialize()
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/candidate/resume')
async def upload_resume(file: UploadFile):
    if not file.filename or not file.filename.lower().endswith('.pdf'): raise HTTPException(400,'Upload a PDF resume.')
    dest=Path('resumes') / 'uploaded_resume.pdf'
    with dest.open('wb') as out: shutil.copyfileobj(file.file,out)
    profile=parse_resume(dest); save_candidate(profile); return profile
@app.get('/candidate')
def candidate():
    profile=get_candidate()
    if not profile: raise HTTPException(404,'No resume has been uploaded.')
    return profile
@app.post('/jobs')
def ingest_job(job: Job): save_job(job); return job
@app.post('/jobs/{job_id}/match')
def score_job(job_id: str):
    candidate=get_candidate()
    if not candidate: raise HTTPException(400,'Upload and review a resume first.')
    from app.database import connection
    with connection() as c: row=c.execute('SELECT data_json FROM jobs WHERE job_id=?',(job_id,)).fetchone()
    if not row: raise HTTPException(404,'Job not found.')
    scored=match(candidate,Job.model_validate_json(row['data_json'])); save_match(scored); return scored
@app.get('/jobs')
def jobs(): return [dict(r) for r in list_rows()]
