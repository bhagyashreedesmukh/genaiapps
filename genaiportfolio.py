import streamlit as st
import openai
import os
import pandas as pd
from PyPDF2 import PdfReader

# Setup
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="GenAI Portfolio", layout="wide")

st.title("🚀 Generative AI Use Case Portfolio")
st.write("Explore 4 sample apps: Meeting Assistant, Requirement Translator, Feedback Analyzer, Regulatory Summarizer")

# Sidebar navigation
page = st.sidebar.radio(
    "Choose a Use Case:",
    [
        "📋 Meeting Intelligence Assistant",
        "📑 Requirement → User Story Translator",
        "📊 Customer Feedback Analyzer",
        "⚖️ Regulatory Change Summarizer"
    ]
)

# ========== 1. Meeting Intelligence ==========
if page == "📋 Meeting Intelligence Assistant":
    st.header("📋 Meeting Intelligence Assistant")
    audio_file = st.file_uploader("Upload Meeting Audio (MP3/WAV)", type=["mp3", "wav"])

    if audio_file:
        st.info("Transcribing audio...")
        transcript = openai.Audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        st.success("Transcription complete ✅")

        st.info("Generating meeting summary...")
        prompt = f"Summarize this meeting into key points, decisions, and action items:\n{transcript['text']}"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message["content"]

        st.subheader("Meeting Summary")
        st.write(summary)

# ========== 2. Requirement Translator ==========
elif page == "📑 Requirement → User Story Translator":
    st.header("📑 Requirement → User Story Translator")
    uploaded_file = st.file_uploader("Upload BRD (PDF)", type=["pdf"])

    if uploaded_file:
        reader = PdfReader(uploaded_file)
        text = " ".join([page.extract_text() for page in reader.pages])

        st.info("Generating User Stories...")
        prompt = f"Convert the following requirements into Agile user stories with acceptance criteria:\n{text}"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        stories = response.choices[0].message["content"]

        st.subheader("Generated User Stories")
        st.write(stories)

# ========== 3. Feedback Analyzer ==========
elif page == "📊 Customer Feedback Analyzer":
    st.header("📊 Customer Feedback Analyzer")
    file = st.file_uploader("Upload CSV with feedback column", type=["csv"])

    if file:
        df = pd.read_csv(file)
        feedback_col = st.selectbox("Select Feedback Column", df.columns)

        results = []
        for fb in df[feedback_col].dropna().head(10):  # limit to 10 for demo
            prompt = f"Analyze the sentiment (Positive, Neutral, Negative) and main theme for this feedback:\n{fb}"
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            results.append(response.choices[0].message["content"])

        st.subheader("Sample Analysis (10 rows)")
        for r in results:
            st.write("- ", r)

# ========== 4. Regulatory Summarizer ==========
elif page == "⚖️ Regulatory Change Summarizer":
    st.header("⚖️ Regulatory Change Summarizer")
    uploaded_file = st.file_uploader("Upload Regulatory Document (PDF)", type=["pdf"])

    if uploaded_file:
        reader = PdfReader(uploaded_file)
        text = " ".join([page.extract_text() for page in reader.pages[:5]])  # first 5 pages only

        st.info("Summarizing...")
        prompt = f"""
        Summarize this regulatory document in plain English.
        Highlight key changes, impacted business processes, and compliance actions required.
        \n{text}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        summary = response.choices[0].message["content"]

        st.subheader("Summary & Impact")
        st.write(summary)
