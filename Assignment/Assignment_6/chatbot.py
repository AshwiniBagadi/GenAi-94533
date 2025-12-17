# Q1: Design a Streamlit-based application with a sidebar to
# switch between Groq and LM Studio. The app should accept 
# a user question and display responses using Groq’s cloud 
# LLM and a locally running LM Studio model.
# Also maintain and display the complete chat history of user 
# questions and model responses.

import os
import requests
import json
import time
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("CHATBOT")

with st.sidebar:
    st.header("Models")
    groq=st.button("GROQ AI", type="primary")
    local=st.button("Local AI", type="primary")



def groq_ai():
    st.subheader("GROQ Based AI")
    api_key1=os.getenv("groq_api")

    url="https://api.groq.com/openai/v1/chat/completions"

    if "message" not in st.session_state:
        st.session_state.message=[]

    while True:
        input=st.chat_input("Ask Anything..")

        if input=="exit":
            break

        headers = {
            "Authorization": f"Bearer {api_key1}",
            "Content-Type": "application/json"
        }

        req_data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                { "role": "user", "content": input }
            ],
        }

        response = requests.post(url, data=json.dumps(req_data), headers=headers)
        print("Status:", response.status_code)

        resp = response.json()
        output=st.write_stream(resp["choices"][0]["message"]["content"])

def local_ai():
    api_key2 = "dummy-key"
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key2}",
        "Content-Type": "application/json"
    }

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    while True:
        user_prompt = st.chat_input("Ask anything: ")
        if user_prompt == "exit":
            break
        req_data = {
            "model": "google/gemma-3-4b",
            "messages": [
                { "role": "user", "content": user_prompt }
            ],
        }
        
        response = requests.post(url, data=json.dumps(req_data), headers=headers)
        
        resp = response.json()
        output=st.write_stream(resp["choices"][0]["message"]["content"])





