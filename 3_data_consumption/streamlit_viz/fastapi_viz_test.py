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

# Load data from FastAPI
st.title("Adzuna German IT-Job Market")
st.sidebar.title("Table of contents")
pages = ["Exploration", "DataVizualization"]
page = st.sidebar.radio("Go to", pages)

st.cache.clear()
#@st.cache_data # prevent unnecessary re-fetching of data
def get_dataframe_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())

try:
    df_ads = get_dataframe_from_url("http://fastapi_app:8000/ads")
    df_salary = get_dataframe_from_url("http://fastapi_app:8000/salary")
    df_salary.columns = df_salary.columns.str.lower()

    if page == "Exploration":
        st.write('### Exploration of Data')
        st.write('##### IT-Job Advertisements')
        st.dataframe(df_ads.head(10))
        st.write('Size of dataset =', df_ads.shape)
        if st.checkbox('Show nans for ads'):
            st.dataframe(df_ads.isna().sum())

        st.write('#####')
        st.write('##### Avg. salary for IT-jobs in selected locations')
        st.dataframe(df_salary.head(10))
        st.write('Size of dataset =', df_salary.shape)
        if st.checkbox('Show nans for salaries'):
            st.dataframe(df_salary.isna().sum())

    elif page == "DataVizualization":
        st.write('### Some Visualizations of Data')
        st.write('##### Overall Development of Job-Ads by month')
        df_ads['created'] = pd.to_datetime(df_ads['created'])
        df_ads['month_year'] = df_ads['created'].dt.to_period('M')
        df_ads = df_ads.sort_values('month_year').reset_index(drop=True)
        jobs_per_month = df_ads['month_year'].value_counts().sort_index()
        jobs_per_month.index = jobs_per_month.index.strftime('%Y-%m')
        st.line_chart(jobs_per_month)

        st.write('##### Top Employers Offering Most Jobs')
        top_employers = df_ads['company'].value_counts()
        st.write(top_employers)

        st.write(df_salary.head(10))
        
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

        # Group by "location" and "job_title" and calculate the average salary for each group
        avg_salary_job = df_salary.groupby(["location", "job_title"])["salary"].mean().reset_index()

        # Sort the data by salary in descending order
        avg_salary_job = avg_salary_job.sort_values(by="salary", ascending=False)

        # Create a grouped bar chart using Altair
        chart_grouped = alt.Chart(avg_salary_job).mark_bar().encode(
            x=alt.X('location:N', axis=alt.Axis(labelAngle=45)),  # Display location on the X-axis
            y=alt.Y('salary:Q'),  # Salary on the Y-axis
            color=alt.Color('job_title:N', legend=alt.Legend(orient='bottom')),  # Different color for each job title
            tooltip=['location', 'job_title', 'salary'],  # Show location, job title, and salary in the tooltip
            column=alt.Column('job_title:N', spacing=10)  # Separate the bars by job title in columns
        ).properties(
            width=250,  # Set the width of each bar group
            height=300,  # Set the height of the chart
        )

        # Display the chart in Streamlit
        st.altair_chart(chart_grouped)


        st.write('#####')
        st.write('##### Development of Avg. Salary in Desired Location')
        display = st.radio('Which location do you want to be shown?', ('Frankfurt', 'Hamburg', 'Munich', 'Cologne', 'Berlin'))

        job_titles = df_salary['job_title'].unique()
        selected_job_titles = st.multiselect('Which jobs would you like to be shown?', job_titles, ['Analyst', 'Engineer', 'Software Developer'])

    if display == 'Frankfurt':
        mask_location = df_salary.loc[:, 'location'] == 'Frankfurt'
        salary_data_F = df_salary.loc[mask_location, :]
        salary_data_F = salary_data_F.sort_values('month').reset_index(drop=True)
        salary_data_F = salary_data_F[salary_data_F['job_title'].isin(selected_job_titles)]
        st.line_chart(data=salary_data_F, x='month', y='salary', color='job_title')

    if display == 'Hamburg':
        mask_location = df_salary.loc[:, 'location'] == 'Hamburg'
        salary_data_HH = df_salary.loc[mask_location, :]
        salary_data_HH = salary_data_HH.sort_values('month').reset_index(drop=True)
        salary_data_HH = salary_data_HH[salary_data_HH['job_title'].isin(selected_job_titles)]
        st.line_chart(data=salary_data_HH, x='month', y='salary', color='job_title')

    if display == 'Munich':
        mask_location = df_salary.loc[:, 'location'] == 'Munich'
        salary_data_M = df_salary.loc[mask_location, :]
        salary_data_M = salary_data_M.sort_values('month').reset_index(drop=True)
        salary_data_M = salary_data_M[salary_data_M['job_title'].isin(selected_job_titles)]
        st.line_chart(data=salary_data_M, x='month', y='salary', color='job_title')

    if display == 'Cologne':
        mask_location = df_salary.loc[:, 'location'] == 'Cologne'
        salary_data_K = df_salary.loc[mask_location, :]
        salary_data_K = salary_data_K.sort_values('month').reset_index(drop=True)
        salary_data_K = salary_data_K[salary_data_K['job_title'].isin(selected_job_titles)]
        st.line_chart(data=salary_data_K, x='month', y='salary', color='job_title')

    if display == 'Berlin':
        mask_location = df_salary.loc[:, 'location'] == 'Berlin'
        salary_data_B = df_salary.loc[mask_location, :]
        salary_data_B = salary_data_B.sort_values('month').reset_index(drop=True)
        salary_data_B = salary_data_B[salary_data_B['job_title'].isin(selected_job_titles)]
        st.line_chart(data=salary_data_B, x='month', y='salary', color='job_title')


except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data from API: {e}")
