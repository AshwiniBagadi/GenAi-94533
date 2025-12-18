import streamlit as st
from langchain.chat_models import init_chat_model
import os
import pandas as pd
import pandasql as ps
from dotenv import load_dotenv

load_dotenv()

st.title("CSV UPLOADER")

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("groq_api")
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

                explanation = llm.invoke(explain_prompt)
                st.subheader("Explanation")
                st.write(explanation.content)

            except Exception as e:
                st.error(f"SQL Execution Error: {e}")
