import json, sqlite3
from pathlib import Path
from app.models import CandidateProfile, Job, Match
DB_PATH = Path('database/job_pipeline.db')
SCHEMA = '''
CREATE TABLE IF NOT EXISTS candidate (id INTEGER PRIMARY KEY CHECK(id=1), profile_json TEXT NOT NULL, updated_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS jobs (job_id TEXT PRIMARY KEY, company TEXT NOT NULL, title TEXT NOT NULL, source TEXT NOT NULL, url TEXT NOT NULL, data_json TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS matches (job_id TEXT PRIMARY KEY REFERENCES jobs(job_id), score REAL NOT NULL, data_json TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY, job_id TEXT NOT NULL REFERENCES jobs(job_id), status TEXT NOT NULL, applied_at TEXT, resume_version TEXT, cover_letter TEXT, UNIQUE(job_id));
'''
def connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True); con=sqlite3.connect(DB_PATH); con.row_factory=sqlite3.Row; return con
def initialize():
    with connection() as c: c.executescript(SCHEMA)
def save_candidate(profile: CandidateProfile):
    with connection() as c: c.execute('INSERT INTO candidate(id,profile_json) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET profile_json=excluded.profile_json, updated_at=CURRENT_TIMESTAMP',(profile.model_dump_json(),))
def get_candidate():
    with connection() as c: row=c.execute('SELECT profile_json FROM candidate WHERE id=1').fetchone()
    return CandidateProfile.model_validate_json(row['profile_json']) if row else None
def save_job(job: Job):
    with connection() as c: c.execute('INSERT INTO jobs(job_id,company,title,source,url,data_json) VALUES(?,?,?,?,?,?) ON CONFLICT(job_id) DO UPDATE SET data_json=excluded.data_json',(job.job_id,job.company,job.job_title,job.source,job.job_url,job.model_dump_json()))
def save_match(match: Match):
    with connection() as c: c.execute('INSERT INTO matches(job_id,score,data_json) VALUES(?,?,?) ON CONFLICT(job_id) DO UPDATE SET score=excluded.score,data_json=excluded.data_json',(match.job_id,match.score,match.model_dump_json()))
def list_rows():
    with connection() as c: return c.execute('SELECT j.data_json, m.data_json AS match_json, a.status FROM jobs j LEFT JOIN matches m USING(job_id) LEFT JOIN applications a USING(job_id) ORDER BY m.score DESC').fetchall()
