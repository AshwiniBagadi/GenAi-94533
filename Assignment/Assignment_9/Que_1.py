# Q1:
# Design and implement a Streamlit-based application consisting of two intelligent agents:
# (1) a CSV Question Answering Agent that allows users to upload a CSV file, display its schema, 
# and answer questions by converting them into SQL queries using pandasql

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import streamlit as st
import os
import json
import requests
import pandas as pd
import pandasql as ps

load_dotenv()

st.title("CSV UPLOADER")

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api")
)

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="You are a helpful assistant. Answer in short."
)

csv_file = st.file_uploader("Upload a CSV file", type="csv")

if csv_file is not None:
    df = pd.read_csv(csv_file)

    st.subheader("CSV Schema")
    st.write(df.dtypes)

    user_input = st.chat_input("Ask anything about this CSV")

    if user_input:
        llm_input = f"""
        Table name: data
        Table schema:
        {df.dtypes}

        Question: {user_input}

        Instructions:
        1. Convert the question into a valid SQLite SQL query.
        2. Use only the table name `data`.
        3. Return ONLY the SQL query.
        4. If not possible, return 'Error'.
        """

        sql_query = llm.invoke(llm_input).content.strip()

        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")

        if sql_query.lower() != "error":
            try:
                result_df = ps.sqldf(sql_query, {"data": df})

                st.subheader("Query Result")
                st.dataframe(result_df)

                explain_prompt = f"""
                SQL Query Result:
                {result_df.head()}

                Explain the result in simple English in 2-3 lines.
                """

                explanation = agent.invoke(explain_prompt)
                st.subheader("Explanation")
                st.success(explanation.content)

            except Exception as e:
                st.error(f"SQL Execution Error: {e}")

