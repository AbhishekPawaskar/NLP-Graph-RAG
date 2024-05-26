import os
import sys
import requests
import streamlit as st

url = os.environ.get("BACKEND_CHAT_URL")

def make_request(query:str):
    try:
        payload = {"userId": "1234","query": query}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["queryResponse"]
        else:
            sys.stdout.write(str(response.status_code))
            return "Failed to generate Response please Try Again"
    except Exception as e:
        sys.stdout.write(str(e))
        return "Failed to generate Response please Try Again"

if __name__ == "__main__":
    st.title("NLP GRAPH RAG")

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    user_input = st.text_input("Query:", key="user_input")
    print(user_input)
    temp_input = user_input

    if st.button("Send"):
        if temp_input:
            response_data = make_request(query=temp_input)
            st.session_state.messages.append(("Response", response_data))
            st.session_state.messages.append(("Query", temp_input))
            # st.session_state.user_input = ""

    for sender, message in reversed(st.session_state.messages):
        if sender == "Query":
            st.markdown(f"**Query:** {message}")
        else:
            st.markdown(f"**Response:** {message}")
