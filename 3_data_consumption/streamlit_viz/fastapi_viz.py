import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import altair as alt
import requests
import json
import os

#load data from fastapi

try:
    response = requests.get("http://fastapi_app:8000/ads")
    response.raise_for_status()
    data = response.json()
    
    df_ads = pd.DataFrame(data)
      
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data from API: {e}")

try:
    response = requests.get("http://fastapi_app:8000/salary")
    response.raise_for_status()
    data = response.json()
    
    df_salary = pd.DataFrame(data)
      
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data from API: {e}")

st.title("Adzuna German IT-Job Market")
st.sidebar.title("Table of contents")
pages=["Exploration", "DataVizualization", "Modelling"]
page=st.sidebar.radio("Go to", pages)

if page == pages[0] : 
  st.write('### Exploration of Data')
  st.write('#####')
  st.write('##### IT-Job Advertisements')
  st.dataframe(df_ads.head(10))
  st.write('Size of dataset =', df_ads.shape)
  if st.checkbox('Show nans for ads'):
    st.dataframe(df_ads.isna().sum())  

  st.write('#####')
  st.write('##### Avg. Salary for IT-jobs in selected locations')
  st.dataframe(df_salary.head(10))
  st.write('Size of dataset =', df_salary.shape)
  if st.checkbox('Show nans for salaries'):
    st.dataframe(df_salary.isna().sum())  

if page == pages[1] :
  st.write('### Some Vizualizations of Data')
  st.write('#####')
  st.write('##### Overall Development of Job-Ads by Month')
  df_ads['created'] = pd.to_datetime(df_ads['created'])
  df_ads['month_year'] = df_ads['created'].dt.to_period('M')
  df_ads = df_ads.sort_values('month_year').reset_index(drop=True)
  jobs_per_month = df_ads['month_year'].value_counts()
  jobs_per_month.index = jobs_per_month.index.strftime('%Y-%m')
  st.line_chart(data = jobs_per_month)

  st.write('#####')
  st.write('##### Top Empoyers Offering Most Jobs for the Time Being...')
  top_employers = df_ads['company'].value_counts()
  st.write(top_employers)
  
  st.write('#####')
  st.write('##### Top 5 populated German cities and their 24M avrg. salary for the jobs: Analyst, Engineer and Software Developer')
  avg_salary = df_salary.groupby("Location")["Salary"].mean().reset_index()
  avg_salary = avg_salary.sort_values(by="Salary", ascending=False)
  chart = alt.Chart(avg_salary).mark_bar().encode(
      x=alt.X('Location:N', sort='-y', axis=alt.Axis(labelAngle=45)),
      y='Salary:Q',
      tooltip=['Location', 'Salary']
  ).properties(
      width=600,
      height=400,
      title='Average Salary by Location'
  )
  st.altair_chart(chart)
  
  st.write('#####')
  st.write('##### Average Salary by Location and Job Title (24M Average)')
  avg_salary_job = df_salary.groupby(["Location", "Job Title"])["Salary"].mean().reset_index()
  avg_salary_job = avg_salary_job.sort_values(by="Salary", ascending=False)
  chart_grouped = alt.Chart(avg_salary_job).mark_bar().encode(
      x=alt.X('Location:N', axis=alt.Axis(labelAngle=45)),
      y=alt.Y('Salary:Q'),
      color=alt.Color('Job Title:N', legend=alt.Legend(orient='bottom')),
      tooltip=['Location', 'Job Title', 'Salary'],
      column=alt.Column('Job Title:N', spacing=10)
  ).properties(
      width=250,
      height=300,
  )
  st.altair_chart(chart_grouped)
  
  st.write('#####')
  st.write('##### Development of Avg. Salary in Desired Location')
  display = st.radio('Which location do you want to be shown?', ('Frankfurt', 'Hamburg', 'Munich', 'Cologne', 'Berlin'))

  job_titles = df_salary['Job Title'].unique()
  if not len(job_titles):
    st.warning("Select at least one Job!")
  selected_job_titles = st.multiselect('Which jobs would you like to be shown?', job_titles, ['Analyst', 'Engineer', 'Software Developer'])

  if display == 'Frankfurt':
    mask_location = df_salary.loc[:, 'Location'] == 'Frankfurt'
    salary_data_F = df_salary.loc[mask_location, :]
    salary_data_F = salary_data_F.sort_values('Month').reset_index(drop=True)
    salary_data_F = salary_data_F[salary_data_F['Job Title'].isin(selected_job_titles)]
    st.line_chart(data = salary_data_F, x='Month', y='Salary', color='Job Title',)

  if display == 'Hamburg':
    mask_location = df_salary.loc[:, 'Location'] == 'Hamburg'
    salary_data_HH = df_salary.loc[mask_location, :]
    salary_data_HH = salary_data_HH.sort_values('Month').reset_index(drop=True)
    salary_data_HH = salary_data_HH[salary_data_HH['Job Title'].isin(selected_job_titles)]
    st.line_chart(data = salary_data_HH, x='Month', y='Salary', color='Job Title',)

  if display == 'Munich':
    mask_location = df_salary.loc[:, 'Location'] == 'Munich'
    salary_data_M = df_salary.loc[mask_location, :]
    salary_data_M = salary_data_M.sort_values('Month').reset_index(drop=True)
    salary_data_M = salary_data_M[salary_data_M['Job Title'].isin(selected_job_titles)]
    st.line_chart(data = salary_data_M, x='Month', y='Salary', color='Job Title',)

  if display == 'Cologne':
    mask_location = df_salary.loc[:, 'Location'] == 'Cologne'
    salary_data_K = df_salary.loc[mask_location, :]
    salary_data_K = salary_data_K.sort_values('Month').reset_index(drop=True)
    salary_data_K = salary_data_K[salary_data_K['Job Title'].isin(selected_job_titles)]
    st.line_chart(data = salary_data_K, x='Month', y='Salary', color='Job Title',)

  if display == 'Berlin':
    mask_location = df_salary.loc[:, 'Location'] == 'Berlin'
    salary_data_B = df_salary.loc[mask_location, :]
    salary_data_B = salary_data_B.sort_values('Month').reset_index(drop=True)
    salary_data_B = salary_data_B[salary_data_B['Job Title'].isin(selected_job_titles)]
    st.line_chart(data = salary_data_B, x='Month', y='Salary', color='Job Title',)

if page == pages[2] : 
  st.write('### Modelling Decision Support...')
  st.write('#####')
  st.write('##### ...tbd')