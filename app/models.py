from __future__ import annotations
from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl

class CandidateProfile(BaseModel):
    name: str | None = None; email: str | None = None; phone: str | None = None
    location: str | None = None; linkedin: str | None = None; github: str | None = None
    years_of_experience: float | None = None; professional_summary: str | None = None
    skills: list[str] = Field(default_factory=list); work_experience: list[dict] = Field(default_factory=list)
    projects: list[dict] = Field(default_factory=list); education: list[dict] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list); raw_text: str = ""

class Job(BaseModel):
    job_id: str; job_title: str; company: str; country: str | None = None; city: str | None = None
    work_mode: Literal['remote','hybrid','onsite','unknown'] = 'unknown'; experience_required: str | None = None
    required_skills: list[str] = Field(default_factory=list); preferred_skills: list[str] = Field(default_factory=list)
    salary: str | None = None; visa_sponsorship: str | None = None; job_url: str; application_url: str | None = None
    full_job_description: str; date_posted: date | None = None; source: str

class Match(BaseModel):
    job_id: str; score: float; matching_skills: list[str]; missing_skills: list[str]
    explanation: str; risks: list[str]; qualified: bool
