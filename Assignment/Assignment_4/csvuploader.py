# 2. For unauthenticated users, show menu (in sidebar) as Home, Login,
# Register. Keep login details in users.csv. For authenticated users, show
# menu explore CSV, See history, Logout. Maintain CSV upload history
# (userid, csv file name, date-time of upload) into userfiles.csv. Use pandas
# for reading/writing data CSVs.

import streamlit as st
import pandas as pd
import pandasql as ps

st.title("CSV UPLOADER")

if "page" not in st.session_state:
    st.session_state.page="login page"

if "login" not in st.session_state:
    st.session_state.login=False

def home_page():
    if st.session_state.login==True:
        st.subheader("Upload csv files")
        st.file_uploader("upload file", type="csv")

def login_page():
    if st.session_state.login==False:
        with st.form("Login"):
            username=st.text_input("username")
            password=st.text_input("Password", type="password")
            submit=st.form_submit_button("Submit")
            if submit:
                st.session_state.login=True


def register():
    st.subheader("Register")
    with st.form("Register"):
        with st.form("Login"):
            username=st.text_input("username")
            password=st.text_input("Password", type="password")
            submit=st.form_submit_button("Submit")


with st.sidebar:
    if st.button("Home", width="stretch"):
        st.session_state.page="home page"
    if st.button("Login", width="stretch"):
        st.session_state.page="login page"
    if st.button("Register", width="stretch"):
        st.session_state.page="register"

if st.session_state.page== "home page":
    home_page()
elif st.session_state.page=="login page":
    login_page()
elif st.session_state.page=="register":
    register()