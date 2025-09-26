if uploaded_audio:
    progress = st.progress(0)
    status = st.empty()

    # Step 1: Transcription
    status.text("Step 1/3: Transcribing audio...")
    text = transcribe_audio(uploaded_audio)
    progress.progress(33)

    # Step 2: Summarization
    status.text("Step 2/3: Summarizing meeting...")
    summary = call_openai(f"Summarize this meeting:\n\n{text}", max_tokens=200)
    progress.progress(66)

    # Step 3: Action items
    status.text("Step 3/3: Extracting action items...")
    actions = call_openai(f"Extract action items from this meeting:\n\n{text}", max_tokens=150)
    progress.progress(100)

    status.text("✅ Done! Meeting processed successfully.")

    # Display results
    st.subheader("✨ Summary")
    st.write(summary)
    st.subheader("📝 Action Items")
    st.write(actions)

    # Export report content
    report_content = {"Summary": summary, "Action Items": actions, "Transcript": text}

    # --- Download buttons appear only here ---
    docx_file = "meeting_report.docx"
    export_to_docx(docx_file, report_content, title="Meeting Report")
    with open(docx_file, "rb") as f:
        st.download_button(
            "⬇️ Download Word Report",
            f,
            file_name=docx_file,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    pdf_file = "meeting_report.pdf"
    export_to_pdf(pdf_file, report_content, title="Meeting Report")
    with open(pdf_file, "rb") as f:
        st.download_button(
            "⬇️ Download PDF Report",
            f,
            file_name=pdf_file,
            mime="application/pdf"
        )
