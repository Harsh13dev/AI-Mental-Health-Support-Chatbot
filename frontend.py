import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout='wide')
st.title("SafeSpace - AI Mental Health Therapist")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("What's on your mind today?")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    response = requests.post(BACKEND_URL, json={"message": user_input})

    response_data = response.json()
    final_response = response_data["response"]

    if isinstance(final_response, list) and len(final_response) > 0 and 'text' in final_response[0]:
        display_content = final_response[0]['text']
    else:
        display_content = final_response
    
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": f'{display_content} WITH TOOL: [{response_data["tool_called"]}]'
    })

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])