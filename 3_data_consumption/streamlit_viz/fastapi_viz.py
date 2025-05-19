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
import sys
import warnings


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
pages=["Exploration", "DataVizualization"]
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
  st.dataframe(df_salary)
  st.write('Size of dataset =', df_salary.shape)
  if st.checkbox('Show nans for salaries'):
    st.dataframe(df_salary.isna().sum())  

if page == pages[1] :
  st.write('### Some Vizualizations of Data')
  st.write('#####')
  st.write('##### Overall Development of Job-Ads by week since 2025 (creation date)')
  df_ads['created'] = pd.to_datetime(df_ads['created'])
  # Filter to only include 2025 and later
  df_ads = df_ads[df_ads['created'] >= '2025-01-01']
  # Group by ISO week (Year-Week)
  df_ads['year_week'] = df_ads['created'].dt.strftime('%Y-%U')
  jobs_per_week = df_ads['year_week'].value_counts().sort_index()
  st.line_chart(data=jobs_per_week)

  st.write('#####')
  st.write('##### Top Employers Offering Most Jobs for the Time Being...')
  top_employers = df_ads['company'].value_counts()
  st.write(top_employers)
  
  st.write('#####')
  st.write('##### Top 5 populated German cities and their 24M avrg. salary for the jobs: Analyst, Engineer and Software Developer')
  avg_salary = df_salary.groupby("location")["salary"].mean().reset_index()
  avg_salary = avg_salary.sort_values(by="salary", ascending=False)
  chart = alt.Chart(avg_salary).mark_bar().encode(
      x=alt.X('location:N', sort='-y', axis=alt.Axis(labelAngle=45)),
      y='salary:Q',
      tooltip=['location', 'salary']
  ).properties(
      width=600,
      height=400,
      title='Average Salary by Location'
  )
  st.altair_chart(chart)
  
  st.write('#####')
  st.write('##### Average Salary by Location and Job Title (24M Average)')
  avg_salary_job = df_salary.groupby(["location", "job_title"])["salary"].mean().reset_index()
  avg_salary_job = avg_salary_job.sort_values(by="salary", ascending=False)
  chart_grouped = alt.Chart(avg_salary_job).mark_bar().encode(
      x=alt.X('location:N', axis=alt.Axis(labelAngle=45)),
      y=alt.Y('salary:Q'),
      color=alt.Color('job_title:N', legend=alt.Legend(orient='bottom')),
      tooltip=['location', 'job_title', 'salary'],
      column=alt.Column('job_title:N', spacing=10)
  ).properties(
      width=250,
      height=300,
  )
  st.altair_chart(chart_grouped)
  
  st.write('#####')
  st.write('##### Development of Avg. Salary in Desired Location')
  display = st.radio('Which location do you want to be shown?', ('Frankfurt', 'Hamburg', 'Munich', 'Cologne', 'Berlin'))

  job_titles = df_salary['job_title'].unique()
  if not len(job_titles):
    st.warning("Select at least one Job!")
  selected_job_titles = st.multiselect('Which jobs would you like to be shown?', job_titles, ['Analyst', 'Engineer', 'Software Developer'])

  if display == 'Frankfurt':
    mask_location = df_salary.loc[:, 'location'] == 'Frankfurt'
    salary_data_F = df_salary.loc[mask_location, :]
    salary_data_F = salary_data_F.sort_values('month').reset_index(drop=True)
    salary_data_F = salary_data_F[salary_data_F['job_title'].isin(selected_job_titles)]
    st.line_chart(data = salary_data_F, x='month', y='salary', color='job_title',)

  if display == 'Hamburg':
    mask_location = df_salary.loc[:, 'location'] == 'Hamburg'
    salary_data_HH = df_salary.loc[mask_location, :]
    salary_data_HH = salary_data_HH.sort_values('month').reset_index(drop=True)
    salary_data_HH = salary_data_HH[salary_data_HH['job_title'].isin(selected_job_titles)]
    st.line_chart(data = salary_data_HH, x='month', y='salary', color='job_title',)

  if display == 'Munich':
    mask_location = df_salary.loc[:, 'location'] == 'Munich'
    salary_data_M = df_salary.loc[mask_location, :]
    salary_data_M = salary_data_M.sort_values('month').reset_index(drop=True)
    salary_data_M = salary_data_M[salary_data_M['job_title'].isin(selected_job_titles)]
    st.line_chart(data = salary_data_M, x='month', y='salary', color='job_title',)

  if display == 'Cologne':
    mask_location = df_salary.loc[:, 'location'] == 'Cologne'
    salary_data_K = df_salary.loc[mask_location, :]
    salary_data_K = salary_data_K.sort_values('month').reset_index(drop=True)
    salary_data_K = salary_data_K[salary_data_K['job_title'].isin(selected_job_titles)]
    st.line_chart(data = salary_data_K, x='month', y='salary', color='job_title',)

  if display == 'Berlin':
    mask_location = df_salary.loc[:, 'location'] == 'Berlin'
    salary_data_B = df_salary.loc[mask_location, :]
    salary_data_B = salary_data_B.sort_values('month').reset_index(drop=True)
    salary_data_B = salary_data_B[salary_data_B['job_title'].isin(selected_job_titles)]
    st.line_chart(data = salary_data_B, x='month', y='salary', color='job_title',)
