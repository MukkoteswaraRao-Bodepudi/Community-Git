"""Resume ingestion: preserves only text evidenced by the supplied PDF."""
import re
from pathlib import Path
from pypdf import PdfReader
from app.models import CandidateProfile
EMAIL=re.compile(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}')
PHONE=re.compile(r'(?:\+?\d[\d .()-]{7,}\d)')
URL=re.compile(r'https?://[^\s|]+|(?:linkedin\.com/in|github\.com)/[^\s|]+',re.I)
def extract_pdf_text(path: str | Path) -> str:
    return '\n'.join(page.extract_text() or '' for page in PdfReader(str(path)).pages)
def parse_resume(path: str | Path) -> CandidateProfile:
    text=extract_pdf_text(path); lines=[x.strip() for x in text.splitlines() if x.strip()]
    urls=URL.findall(text); email=(EMAIL.search(text).group() if EMAIL.search(text) else None); phone=(PHONE.search(text).group() if PHONE.search(text) else None)
    # Conservative extraction: no inferred skills/experience. Review fields in API before applying.
    return CandidateProfile(name=lines[0] if lines else None,email=email,phone=phone,linkedin=next((u for u in urls if 'linkedin' in u.lower()),None),github=next((u for u in urls if 'github' in u.lower()),None),raw_text=text)
