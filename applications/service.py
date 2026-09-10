import os
from app.database import connection
from app.models import CandidateProfile, Job, Match
def decision(match: Match) -> str: return 'prepare_for_permitted_submission' if match.score>=90 else ('manual_review' if match.score>=80 else 'not_qualified')
def create_application(job: Job, candidate: CandidateProfile, match: Match, cover_letter: str=''):
    status=decision(match)
    with connection() as c:
        c.execute('INSERT INTO applications(job_id,status,resume_version,cover_letter) VALUES(?,?,?,?)',(job.job_id,status,'uploaded resume',cover_letter))
    return status
