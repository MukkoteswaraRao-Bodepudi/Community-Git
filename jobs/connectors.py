"""Terms-aware discovery connectors. Official APIs/feeds only; no CAPTCHA/MFA bypass."""
from abc import ABC, abstractmethod
from urllib.parse import urlparse
import hashlib
import httpx
from bs4 import BeautifulSoup
from app.models import Job
class JobConnector(ABC):
    source: str
    @abstractmethod
    async def discover(self, query: str) -> list[Job]: ...
class GreenhouseConnector(JobConnector):
    source='greenhouse'
    def __init__(self, board_token: str): self.board_token=board_token
    async def discover(self, query: str) -> list[Job]:
        url=f'https://boards-api.greenhouse.io/v1/boards/{self.board_token}/jobs?content=true'
        async with httpx.AsyncClient(timeout=20) as c: data=(await c.get(url)).json()['jobs']
        return [normalize_api_job(x,self.source) for x in data if query.lower() in x.get('title','').lower()]
class LeverConnector(JobConnector):
    source='lever'
    def __init__(self, site: str): self.site=site
    async def discover(self, query: str) -> list[Job]:
        async with httpx.AsyncClient(timeout=20) as c: data=(await c.get(f'https://api.lever.co/v0/postings/{self.site}?mode=json')).json()
        return [normalize_api_job(x,self.source) for x in data if query.lower() in x.get('text','').lower()]
class RestrictedConnector(JobConnector):
    """LinkedIn, Indeed, Wellfound, Workday and career sites require an approved API/feed adapter."""
    def __init__(self, source): self.source=source
    async def discover(self, query): return []
def normalize_api_job(raw, source):
    title=raw.get('title') or raw.get('text',''); url=raw.get('absolute_url') or raw.get('hostedUrl') or raw.get('applyUrl','')
    content=raw.get('content','') or raw.get('descriptionPlain','')
    return Job(job_id=hashlib.sha256((source+url).encode()).hexdigest()[:20],job_title=title,company='',job_url=url,application_url=raw.get('applyUrl',url),full_job_description=BeautifulSoup(content,'html.parser').get_text(' ',strip=True),source=source)
