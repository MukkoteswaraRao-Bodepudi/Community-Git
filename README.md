# Generative AI Job Automation Pipeline

A consent-first, evidence-based job discovery and review system. It treats the uploaded resume PDF as the sole source of candidate facts: it does not infer skills, work authorization, visa status, education, or experience. No resume is included in this repository; upload yours through the API and review the extracted profile before proceeding.

## Architecture and phases

1. **Resume Parser** (`resumes/parser.py`) extracts PDF text and conservative contact fields; unstructured sections remain in `raw_text` until validated.
2. **Job Discovery** (`jobs/connectors.py`) offers official public Greenhouse and Lever API connectors. LinkedIn, Indeed, Wellfound, Workday, and arbitrary company career sites are deliberately disabled until an approved API/feed adapter and terms review are configured. Robots restrictions, authentication, CAPTCHA, and MFA are never bypassed.
3. **Semantic Matching** (`matching/engine.py`) scores technical skills (35%), responsibilities (25%), GenAI domain (20%), experience (10%), and education (10%). Only scores at least 80 qualify.
4. **Sheets** (`sheets/client.py`) writes the required tracker columns to the Google Sheet configured by environment variables.
5. **Auto Apply** (`applications/service.py`) labels >=90 as `prepare_for_permitted_submission`, 80–89 as `manual_review`, and never performs browser submission. Submission must be separately enabled only for sources that expressly permit it.
6. **Dashboard** (`dashboard/app.py`) displays tracker metrics and country/status/score filters.

## Install and run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
# separate terminal
streamlit run dashboard/app.py
```

Upload: `curl -F 'file=@resume.pdf' http://localhost:8000/candidate/resume`. Then inspect `GET /candidate`; populate only facts visible in your PDF before matching jobs. Start with `POST /jobs` using the schema exposed at `/docs`, then call `POST /jobs/{job_id}/match`.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

API is on `:8000`, Streamlit on `:8501`; SQLite persists in `database/`.

## Google OAuth and Sheets

1. In Google Cloud, enable Google Sheets API and create a service account.
2. Download its JSON key outside source control, then share a spreadsheet named **Generative AI Job Tracker** with the service-account email.
3. Set `GOOGLE_SERVICE_ACCOUNT_FILE` and `GOOGLE_SHEETS_ID` in `.env`.
4. Invoke `sheets.client.sync(rows)` with rows ordered as `sheets.client.HEADERS`. Configure score conditional formatting in the Sheet: green 90–100, yellow 80–89, red <80.

## Data model

SQLite uses `candidate`, `jobs`, `matches`, and `applications`. `jobs.job_id` and `applications.job_id` are unique, preventing duplicate applications. Job payloads retain the requested normalized fields in JSON, and application status/audit fields are relational.

## Safety and operations

Use only authorized APIs and feeds. Log failures at the caller boundary, retry network calls with `tenacity` where connectors are added, and do not supply values for missing candidate fields. Review each application, cover letter, work authorization question, and source automation policy before submission.

## Tests

```bash
pytest -q
```
