from lyzr import DataConnector, DataAnalyzr
from streamlit_extras.grid import grid
from dotenv import load_dotenv
from typing import Optional
import streamlit as st
import shutil
import json
import os


st.set_page_config(layout='wide')
st.subheader('AWS RedShift Analyser with Lyzr')
if 'dataframe' not in st.session_state:
    st.session_state.dataframe = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

with st.sidebar:
    st.caption('Enter the credentials')
    host_url = st.text_input('RedShift URL')
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    with col1:
        username = st.text_input('Username')
    with col2:
        password = st.text_input('Password', type="password")
    with col3:
        db_name = st.text_input('Database')
    with col4:
        schema = st.text_input('Schema')
    with col5:
        table_name = st.text_input('Table')
    with col6:
        st.session_state.api_key = st.text_input('OpenAI API', type='password')
    submitBtn = st.button('Proceed')
    st.caption('@By_ShankeshRajuMS')

if submitBtn:
    st.session_state.dataframe = DataConnector().fetch_dataframe_from_redshift(
        host=host_url,  # Replace with the actual host of your Redshift Database
        database=db_name,  # Replace with the name of your Redshift Database
        user=username,  # Replace with your Redshift username
        password=password,  # Replace with your Redshift password
        schema=schema,  # Replace with the schema containing the target table
        table=table_name,  # Replace with the name of the table to fetch data from
        port=5439,  # Replace with the appropriate port number for your Redshift Database
    )
col1, col2 = st.columns([0.8, 0.2], gap='large')
with col1:
    if st.session_state.dataframe is not None:
        st.dataframe(st.session_state.dataframe)
    else:
        st.write('Enter credentials to view the database')

with col2:
    st.caption('Suggestions')

    # mygrid = grid(3, 1, 2, vertical_align="bottom")
    # data_desc = mygrid.button('Data Description')
    # analysis_query = mygrid.button('Exploratory Analysis')
    # analysis_recom = mygrid.button('Recommended Analysis')
    data_desc = st.button('Data Description')
    analysis_recom = st.button('Recommendation')
    analysis_query = st.button('Exploratory Analysis')

    st.divider()
    st.caption('User Queries')
    user_input = st.text_input('Enter the query?')

    user_query = st.button('Text Query')
    tasks_query = st.button('Create Tasks')
    visual_query = st.button('Visualization Query')
    recomm_insights = st.button('Analysis and Optimize')


try:
    data_analyzr = DataAnalyzr(df=st.session_state.dataframe, api_key=st.session_state.api_key)
except:
    print('load credentials')
st.divider()
if user_query:
    analysis = data_analyzr.analysis_insights(user_input=user_input)
    st.markdown(user_input)
    st.code(analysis)
if analysis_recom:
    analysis_recommendation = data_analyzr.analysis_recommendation(user_input)
    st.markdown('Recommendations')
    st.code(analysis_recommendation)
if data_desc:
    description = data_analyzr.dataset_description()
    st.markdown("Data Description")
    st.code(description)
if analysis_query:
    queries = data_analyzr.ai_queries_df()
    st.markdown("Exploratory Analysis")
    st.code(queries)
if tasks_query:
    tasks = data_analyzr.tasks(user_input=user_input)
    st.markdown(user_input)
    st.text(tasks)
if recomm_insights:
    recommendations = data_analyzr.recommendations(user_input=user_input)
    st.markdown(user_input)
    st.code(recommendations)
if visual_query:
    try:
        shutil.rmtree('./generated_plots')
    except:
        print('no plots generated')
    visualization = data_analyzr.visualizations(user_input=user_input)
    st.markdown(user_input)
    folder = "./generated_plots"
    for images in os.listdir(folder):
        if images.endswith('.png'):
            st.image(f"./generated_plots/{images}")


  
