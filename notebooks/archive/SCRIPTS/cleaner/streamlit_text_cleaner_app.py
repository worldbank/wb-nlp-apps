import streamlit as st
import pandas as pd
import numpy as np
from phoenix.cleaner import cleaner
from phoenix.detectors import detector
from wordcloud import WordCloud
import time
import plotly
import plotly.express as pxp

# 10.177.202.170:8501

st.title('Text Document Cleaner App')

input_type = st.sidebar.radio(
    'Select Data Input Method',
    options=('Text Input', 'File Upload')
)
st.sidebar.markdown('------')
show_wordcloud = st.sidebar.checkbox('Show wordcloud')
use_spellchecker = st.sidebar.checkbox('Use spell checker')
use_respeller = st.sidebar.checkbox('Use respeller')
use_lemmatizer = st.sidebar.checkbox('Use lemmatizer')
spell_threshold = st.sidebar.number_input('Spell threshold', value=0.7, min_value=0.0, max_value=1.0)
ignore_length = st.sidebar.number_input('Ignore length', value=0, min_value=0)
st.sidebar.markdown('------')

cleaner = cleaner.Cleaner(
    use_spellchecker=use_spellchecker,
    use_respeller=use_respeller,
    use_lemmatizer=use_lemmatizer,
    ignore_length=ignore_length,
    spell_threshold=spell_threshold
)

president_detector = detector.Detector(map_file='../whitelists/wb_presidents.csv')
country_detector = detector.Detector(map_file='../whitelists/whitelist_countries_multilingual.csv', index_col=1)

text = ''

if input_type == 'Text Input':
    default_text = '''The World Bank Group is one of the world’s largest sources of funding and knowledge for developing countries. Its five institutions share a commitment to reducing poverty, increasing shared prosperity, and promoting sustainable development.'''
    text = st.text_area('Input text here:', value=default_text)

elif input_type == 'File Upload':
    text_file = st.file_uploader('Select file to upload', type='txt')
    if text_file:
        text = text_file.read()
        
st.markdown('------')

if text:
    all_stopwords = []
    with st.spinner('Processing data...'):
        time.sleep(1)
        presidents_count = president_detector.detect_entity(text)
        countries_count = country_detector.detect_entity(text)
        
        payload = cleaner.clean_text(text)
        if show_wordcloud:
            st.markdown('### Cleaned Text Word Cloud')
            wordcloud = WordCloud(
                width=600, height=450,
                max_words=200,
                stopwords=all_stopwords,
                background_color ='white', 
                random_state=1029,
                # min_font_size = 10
            ).generate(payload['text'])

            st.image(wordcloud.to_image())

            st.markdown('------')
        
        st.markdown('### Cleaned text:')
        payload['text']
        
        ## Define sidebar data
        st.sidebar.markdown('# Extracted data')
        
        if presidents_count:
            presidents_count = pd.Series(presidents_count, name='Counts').sort_values(ascending=False)
            presidents_count.rename_axis(index='WB President', inplace=True)
            st.sidebar.markdown('### WB Presidents')
            st.sidebar.dataframe(presidents_count)
            
        if countries_count:
            countries_count = pd.Series(countries_count, name='Counts').sort_values(ascending=False)
            countries_count.rename_axis(index='Country', inplace=True)
            st.sidebar.markdown('### Countries')
            st.sidebar.dataframe(countries_count)
            
        st.sidebar.markdown(f"Detected language: {', '.join([i for i in payload['lang'] if isinstance(i, str)])}")
        st.sidebar.markdown(f"Tokens after cleaning: {payload['token']}")

        if payload['spell_errors']:
            se = pd.DataFrame()
            se['Spell Errors'] = payload['spell_errors'] 
            st.sidebar.markdown(f"### Spell errors")
            st.sidebar.dataframe(se)
