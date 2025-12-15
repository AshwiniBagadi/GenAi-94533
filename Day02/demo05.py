import streamlit as st

if 'message' not in st.session_state:
    st.session_state.messages=[]

with st.sidebar:
    st.header("Settings")
    choices=["Upper","Lower","Toggle"]
    mode=st.selectbox("Select Mode",choices)
    count= st.slider("Message Count",0,10,4,2)

    st.subheader("Config")
    st.json({"mode": mode, "count": count})

st.title("CHATBOT")

msg=st.chat_input("Say something...")
if msg:
    outmsg=msg
    if mode=="Upper":
        outmsg=msg.upper()
    elif mode=="Lower":
        outmsg=msg.lower()
    elif mode=="Toggle":
        outmsg=msg.swapcase()

    st.session_state.messages.append(msg)
    st.session_state.messages.append(outmsg)

    msglist=st.session_state.messages
    for idx,message in enumerate(msglist):
        role="Human" if idx%2==0 else "AI"
        with st.chat_message(role):
            st.write(message)
