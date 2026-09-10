import json, streamlit as st
from app.database import initialize, list_rows
initialize(); rows=list_rows(); data=[]
for r in rows:
    j=json.loads(r['data_json']); m=json.loads(r['match_json']) if r['match_json'] else {}; data.append({**j,'score':m.get('score',0),'status':r['status'] or 'new'})
st.title('Generative AI Job Tracker')
st.metric('Jobs Found',len(data)); st.metric('Qualified Jobs',sum(x['score']>=80 for x in data)); st.metric('Applied',sum(x['status']=='submitted' for x in data)); st.metric('Interviews',sum(x['status']=='interview' for x in data)); st.metric('Offers',sum(x['status']=='offer' for x in data))
country=st.selectbox('Country',['All']+sorted({x.get('country') or 'Unknown' for x in data})); minimum=st.slider('Minimum match score',0,100,80); status=st.selectbox('Status',['All']+sorted({x['status'] for x in data}))
st.dataframe([x for x in data if (country=='All' or (x.get('country') or 'Unknown')==country) and x['score']>=minimum and (status=='All' or x['status']==status)],use_container_width=True)
