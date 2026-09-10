"""Semantic match engine. Candidate facts are never augmented from a job post."""
from app.models import CandidateProfile, Job, Match
TARGET_TITLES=('generative ai engineer','genai engineer','ai engineer','llm engineer','rag engineer','ai application engineer','applied ai engineer','conversational ai engineer','agentic ai engineer')
def _tokens(text): return {x.lower() for x in text.replace('/',' ').replace(',',' ').split() if len(x)>1}
def title_relevant(title: str) -> bool:
    t=title.lower(); return any(x in t for x in TARGET_TITLES) or ('ai' in t and 'engineer' in t)
def match(candidate: CandidateProfile, job: Job) -> Match:
    candidate_skills={s.lower():s for s in candidate.skills}; required={s.lower() for s in job.required_skills}; preferred={s.lower() for s in job.preferred_skills}
    matched=sorted(candidate_skills[k] for k in required|preferred if k in candidate_skills); missing=sorted(s for s in job.required_skills if s.lower() not in candidate_skills)
    skill_score=(len(set(x.lower() for x in matched)&required)/len(required)*35 if required else 17.5)
    resume_tokens=_tokens(candidate.raw_text); jd_tokens=_tokens(job.full_job_description)
    responsibility=25*len(resume_tokens&jd_tokens)/max(1,len(jd_tokens))
    genai_terms={'llm','rag','generative','langchain','transformer','prompt','agent','vector','faiss'}
    domain=20*len(genai_terms&resume_tokens&jd_tokens)/len(genai_terms)
    experience=10 if candidate.years_of_experience is not None else 0
    education=10 if candidate.education else 0
    score=round(min(100,skill_score+responsibility+domain+experience+education),2)
    risks=[]
    if missing: risks.append('Required skills not evidenced by the resume: '+', '.join(missing))
    if candidate.years_of_experience is None: risks.append('Years of experience were not explicitly extracted.')
    if not title_relevant(job.job_title): risks.append('Title has low target-role relevance.')
    return Match(job_id=job.job_id,score=score,matching_skills=matched,missing_skills=missing,qualified=score>=80,risks=risks,explanation=f'Skills {skill_score:.1f}/35, responsibilities {responsibility:.1f}/25, GenAI {domain:.1f}/20, experience {experience}/10, education {education}/10.')
