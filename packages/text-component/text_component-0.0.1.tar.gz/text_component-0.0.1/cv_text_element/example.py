import numpy as np 
import streamlit as st
from __init__ import cv_text_el

st.set_page_config(layout="wide")

data = [
    {
        "index":0,
        "label":"Professional Summary",
        "match":"19%"
    },
    {
        "index":0,
        "label":"Professional Summary",
        "match":"select a job"
    }
]

with st.columns(2)[0]:
  with st.columns(2)[0]:
    cv_text_el(data=data)