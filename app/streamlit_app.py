import streamlit as st

import requests

API_URL = "http://api:8000/"

st.title('App Streamlit que consome API FastAPI')

response = requests.get(API_URL)

st.write(response.json())