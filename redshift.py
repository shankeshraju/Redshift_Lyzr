from lyzr import DataConnector, DataAnalyzr
import streamlit as st
from dotenv import load_dotenv
load_dotenv()


df = DataConnector().fetch_dataframe_from_redshift(
    host="shankesh.723893571330.us-east-1.redshift-serverless.amazonaws.com",  # Replace with the actual host of your Redshift Database
    database="dev",  # Replace with the name of your Redshift Database
    user="shankesh",  # Replace with your Redshift username
    password="Sabhashank1",  # Replace with your Redshift password
    schema="public",  # Replace with the schema containing the target table
    table="titanic",  # Replace with the name of the table to fetch data from
    port=5439,  # Replace with the appropriate port number for your Redshift Database
)

# Initialize a DataAnalyzr instance with the obtained DataFrame and API key
data_analyzr = DataAnalyzr(df=df)
analysis = data_analyzr.analysis_insights(user_input="What information does the database hold?")
print(analysis)
analysis_recommendation = data_analyzr.analysis_recommendation()
print(analysis_recommendation)