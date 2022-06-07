import streamlit as st
import os
import altair as alt
import pandas as pd
import validators
from url_utils import extract_content
from timeseries_utils import generate_dataframe
import torch
import pandas as pd
from transformers import pipeline, AutoTokenizer

st.set_page_config(
    page_title="COVID Semaphore Prediction",
    page_icon="🚦",
)

def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


_max_width_()

st.title("COVID-19 Semaphore Prediction")
st.header("")

st.markdown("## ℹ️ How to use this app?")
st.write(
    """
    - By pasting a URL to any mexican news site and find out the COVID-19's semaphore color for **0**, **2**, **4** and **8 weeks** since the news' publication date
    - 📰 -> 🚦
    """
)
st.markdown("")

st.markdown("## 📰 News Finder")
news_url = st.text_area(
    "Paste the URL of any mexican news site",
    height=50
)
semaphore_button = st.button("Find out semaphore's color")

if semaphore_button:
    if len(news_url) == 0:
        st.warning('Please make sure that you write any URL')
        st.stop()
    if not validators.url(news_url):
        st.warning('Please make sure that you write a valid URL')
        st.stop()
else:
    st.stop()

st.markdown("## 🚦 Semaphore prediction")
data, date = extract_content(news_url)

transformer_model_name = 'dccuchile/bert-base-spanish-wwm-cased'
tokenizer = AutoTokenizer.from_pretrained(transformer_model_name)
transformer_models = ['bondi/bert-semaphore-prediction-w0',
                      'bondi/bert-semaphore-prediction-w2',
                      'bondi/bert-semaphore-prediction-w4',
                      'bondi/bert-semaphore-prediction-w8']
transformer_models_clean = ['bondi/bert-clean-semaphore-prediction-w0',
                            'bondi/bert-clean-semaphore-prediction-w2',
                            'bondi/bert-clean-semaphore-prediction-w4',
                            'bondi/bert-clean-semaphore-prediction-w8']

semaphore_classes = ['Yellow', 'Orange', 'Red', 'Green']
semaphore_labels = ['LABEL_1', 'LABEL_2', 'LABEL_3', 'LABEL_0']
mapping = dict(zip(semaphore_labels, semaphore_classes))

@st.experimental_memo
def get_prediction_vector(text, clean_models=False):
    transformer_pipelines = []
    tokenizer_kwargs = {'padding': True, 'truncation': True, 'max_length': 512}
    if clean_models:
        for model in transformer_models_clean:
            transformer_pipelines.append(pipeline(model=model, tokenizer=tokenizer))
    else:
        for model in transformer_models:
            transformer_pipelines.append(pipeline(model=model, tokenizer=tokenizer))


    def predict(text, pipeline):
        return pipeline(text, **tokenizer_kwargs)[0]['label']


    label_dict = {'W0': None, 'W2': None, 'W4': None, 'W8': None}
    label_vector = [None] * len(transformer_pipelines)
    for i in range(len(transformer_pipelines)):
        label_vector[i] = mapping[predict(text, transformer_pipelines[i])]
    return label_vector


v = get_prediction_vector(data)
df = generate_dataframe(date, v)


def semaphore_condition(val):
    if val == 0:    return "Green"
    if val == 1:    return "Yellow"
    if val == 2:    return "Orange"
    if val == 3:    return "Red"

def add_format(styler):
    styler.format(semaphore_condition)
    return styler

color = {"Green": 'green', 'Yellow': 'yellow', 'Orange':'orange', 'Red':'red'}
def color_bg(s):
    return ['background-color: ' + color[s['semaphore']] for _ in s]


df = df.style.apply(color_bg, axis=1)
st.table(df)
