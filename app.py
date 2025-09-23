import streamlit as st

st.title("🚀 Hello World App")
st.write("Welcome to your first Streamlit app!")

name = st.text_input("Enter your name:")
if name:
    st.success(f"Hello, {name}! 🎉")
