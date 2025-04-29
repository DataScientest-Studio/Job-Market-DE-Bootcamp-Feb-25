import streamlit as st
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Adzuna Visualization")
st.sidebar.title("Table of contents")
pages=["Exploration", "DataVizualization", "Modelling"]
page=st.sidebar.radio("Go to", pages)

try:
    response = requests.get("http://fastapi_app:8000/ads")
    response.raise_for_status()
    data = response.json()
    
    df = pd.DataFrame(data)

    if page == pages[0] : 
      st.write("### Presentation of data")
      st.dataframe(df.head(10))
      
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data from API: {e}")