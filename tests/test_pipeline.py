from app.database import DB_PATH, initialize, save_job, save_candidate
from app.models import CandidateProfile, Job
from matching.engine import match, title_relevant
def test_match_never_invents_skills(tmp_path, monkeypatch):
    candidate=CandidateProfile(skills=['Python','LangChain'],raw_text='Built a RAG application',years_of_experience=2,education=[{'degree':'BSc'}])
    job=Job(job_id='1',job_title='Generative AI Engineer',company='Acme',job_url='https://example.test',source='test',full_job_description='Build RAG applications with Python and LangChain',required_skills=['Python','LangChain','Kubernetes'])
    result=match(candidate,job)
    assert 'Kubernetes' in result.missing_skills
    assert result.score <= 100 and result.qualified == (result.score >= 80)
def test_semantic_title_set():
    assert title_relevant('Senior LLM Engineer')
    assert title_relevant('AI Platform Engineer')
