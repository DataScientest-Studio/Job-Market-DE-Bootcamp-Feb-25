import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

salary = pd.read_csv("../../data_collection/output_files/adzuna_salary_24M.csv")
cat = pd.read_csv("../../data_collection/output_files/adzuna_category.csv")
ads = pd.read_csv("../../data_collection/output_files/combined_adzuna_ads_itjobs.csv")

st.title("Adzuna Visualization")
st.sidebar.title("Table of contents")
pages=["Exploration", "DataVizualization", "Modelling"]
page=st.sidebar.radio("Go to", pages)

if page == pages[0] : 
  st.write("### Presentation of data")
  st.dataframe(salary.head(10))
  st.dataframe(ads.head(10))
  st.dataframe(cat.head(10))