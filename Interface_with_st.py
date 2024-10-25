import streamlit as st 
from InteractiveChat import InteractiveChat

st.title("💬 RoutingLLMs Chatbot")
st.header("Ask me about customers, create meeting or just chat with me!")
#st.caption("🚀 RoutingLLMs Chatbot")

user_input = st.text_input("Enter your message: ")
buttton = st.button("Process")
if buttton:
    st.write("Processing...")
    reply = InteractiveChat(user_input)
    st.write(reply)
