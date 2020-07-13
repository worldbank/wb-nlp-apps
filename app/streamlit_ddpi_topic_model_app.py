import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import plotly
import plotly.express as pxp
import json
import plotly.graph_objects as go
import os
import requests
import io
import json

# https://discuss.streamlit.io/t/how-to-use-streamlit-with-nginx/378/7

def notify(fname, message, verbose=True):
    message = f'{datetime.now()}: {message}'
    with open(fname, 'a+') as fl:
        fl.write(message + '\n')
        
    if verbose:
        print(message)

def get_ddi_json(doc_id, return_json=True):
    # https://microdatalib.worldbank.org/index.php/api/catalog/AFG_2014_FINDEX_v01_M
    url = f'https://microdatalib.worldbank.org/index.php/api/catalog/{doc_id}'
    result = requests.get(url)
    
    if return_json:
        payload = result.json()
    else:
        payload = result.content.decode('utf-8')
        payload = payload.replace('}', '')
        payload = payload.replace('{', '')
        
    return payload


def get_text_topics(raw_text):
    files = {
        'file': io.StringIO(raw_text)
    }
    
    url = f'http://wbes2474:8910/api/lda_doc_topics?corpus_id=WB&model_id=ALL_50&topn_topics=10&total_topic_score=0.8&clean_doc=true'  # &raw_text={raw_text}'
    result = requests.get(url, files=files)
    return result.json()


# http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

cmap = 'RdYlGn'  # matplotlib.colors.LinearSegmentedColormap.from_list("", ["red","green"])

# # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
# for i in range(len(tableau20)):
#     r, g, b = tableau20[i]
#     tableau20[i] = (r / 255., g / 255., b / 255.)


st.title('DDI Topic Inferencer')

st.markdown('<span style="color:silver; font-size: 90%;">Prepared by: Aivin V. Solatorio [asolatorio@worldbank.org | Data Scientist]</span>', unsafe_allow_html=True)
st.markdown('-----')


ddi_id = st.text_input('Input microdatalib id:', value='AFG_2013_ES_v01_M') 

if ddi_id:
    input_type = st.sidebar.radio(
        'Text source:',
        options=('Abstract and Series Info', 'All')
    )
    
    ddi_json = get_ddi_json(ddi_id, return_json=True)
    # text = st.text_area('Content', value=ddi_json)
    study = ddi_json['dataset']['metadata']['study_desc']
    
    if input_type == 'All':
        text = json.dumps(ddi_json)
    elif input_type == 'Abstract and Series Info':    
        text = ' '.join([study['series_statement'].get('series_info', ''), study['study_info'].get('abstract', '')])
    
    topics_json = get_text_topics(text)
    
    # text = st.text_area('Content', value=topics_json)
    
    st.header(ddi_json['dataset']['title'])
    st.markdown(f"**{ddi_json['dataset'].get('nation', '')}**")
    
    st.markdown(study['study_info'].get('abstract', ''))
    
    st.markdown('-----')
    
    topics = pd.DataFrame(topics_json['topics'])

    topics = topics.set_index('topic')
    # topics
    
    topics_list = topics_json['topics']
    
    topic_names = []
    topic_scores = []
    
    for t in topics_list:
        st.subheader(f"Topic {t['topic']} : {100 * t['score']:.2f}%")
        st.markdown(', '.join([w['word'] for w in t['words']]))
        
        topic_names.append(f"Topic {t['topic']}")
        topic_scores.append(np.round(100 * t['score'], 2))

    st.sidebar.markdown('-----')

    fig = go.Figure()
    topic_trace = go.Bar(
        x=topic_scores[::-1],
        y=topic_names[::-1],
        name='Topic share',
        orientation='h',
        hovertemplate = "%{y}: %{x:.2f}%",
    )
    fig.add_traces([topic_trace])
    
    fig.update_layout(
        title='Topic share',
        # showlegend=True,
        width=300,
        # height=400,
        margin=dict(l=10, r=30, t=30, b=20),
        paper_bgcolor='rgb(248, 248, 255, 0)',
        plot_bgcolor='rgb(248, 248, 255, 0)',
    )
    
    st.sidebar.plotly_chart(fig)