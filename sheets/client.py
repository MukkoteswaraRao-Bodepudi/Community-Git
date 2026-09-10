import os
HEADERS=['Job ID','Company','Role','Country','Location','Source','Job URL','Match Score','Matching Skills','Missing Skills','Application Status','Application Date','Resume Version','Cover Letter','Recruiter','Interview Stage','Notes']
def sync(rows):
    """Sync to configured Sheet; credentials are supplied through environment, never stored."""
    import gspread
    from google.oauth2.service_account import Credentials
    path=os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE'); sheet_id=os.environ.get('GOOGLE_SHEETS_ID')
    if not (path and sheet_id): raise RuntimeError('GOOGLE_SERVICE_ACCOUNT_FILE and GOOGLE_SHEETS_ID are required')
    gc=gspread.authorize(Credentials.from_service_account_file(path,scopes=['https://www.googleapis.com/auth/spreadsheets']))
    ws=gc.open_by_key(sheet_id).sheet1; ws.update('A1:Q1',[HEADERS]); ws.append_rows(rows)
    ws.format('H2:H',{'numberFormat':{'type':'NUMBER','pattern':'0.00'}})
    ws.set_basic_filter('A1:Q1')
