import streamlit as st

with st.form("reg_form"):
    st.header("Register Form")
    fname=st.text_input("First name")
    lname=st.text_input("Last name")
    age=st.slider("Age",10,100,25,1)
    addr=st.text_area("Address")
    submit_btn=st.form_submit_button("Submit", type="primary")

if submit_btn:
    err_message=""
    is_error=False
    if not fname:
        is_error=True
        err_message+="First name can not be empty.\n"
    if not lname:
        is_error=True
        err_message+="Last name can not be empty.\n"
    if not addr:
        is_error=True
        err_message+="Address can not be empty.\n"

    if is_error:
        st.error(err_message)
    else:
        message=f"Successfully Registered: {fname} {lname} \nAge: {age}. Living at {addr}"
        st.success(message)