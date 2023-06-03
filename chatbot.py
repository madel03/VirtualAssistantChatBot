import streamlit as st
from streamlit_chat import message
from utils import get_initial_message
from utils import get_chatgpt_response
from utils import update_chat
import os
from dotenv import load_dotenv
load_dotenv()

import openai

#to access the openai Key from .env when running the app locally
#openai.api_key = os.getenv('OPENAI_API_KEY')

#to access the openai key from streamlit cloud secrets
#when deploying the app there, directly from GitHub repo
#the secret module is specific to Streamlit Cloud. It is not recognized by VS
#Thats why I keep it as a comment while running locally.
from streamlit.secrets import SecretManager
openai.api_key = SecretManager.get('OPENAI_API_KEY')

st.title("Stella Arbeláez Velasco")
st.header("Cosmetology Specialist")
st.subheader(":blue[_Lana, Virtual Assistant_]")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Query: ", key="input")

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

if query:
    with st.spinner("One moment, please..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, query)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
