import numpy as np
import pandas as pd
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
title="Playlist Tool"
st.set_page_config(
    # layout="wide",
    page_title=title, page_icon=":minidisc:"
)

st.markdown(f'## {title}')

# LOAD DATA ONCE
@st.experimental_singleton
def load_data():
    pass
# STREAMLIT APP LAYOUT
data = load_data()

