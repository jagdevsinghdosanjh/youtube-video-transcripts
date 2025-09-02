import streamlit as st
import os
from transcribe import transcribe_audio
from youtube_audio_downloader import download_audio
from en_audio_tools import (
    get_audio_duration,
    estimate_transcription_time,
    plot_waveform,
    highlight_keywords,
    save_transcript_as_pdf
)

# -------------------- HEADER --------------------
st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <h1 style='margin-bottom: 0;'>English YouTube Transcriber</h1>
        <p style='margin-top: 0; font-size: 16px;'>by <strong>Jagdev Singh Dosanjh</strong> | 
        <a href='https://dosanjhpubsasr.org' target='_blank'>dosanjhpubsasr.org</a> |
        📧 <a href='mailto:jagdevsinghdosanjh@gmail.com'>jagdevsinghdosanjh@gmail.com</a> |
        📞 8146553307</p>
        <hr>
    </div>
""", unsafe_allow_html=True)

# -------------------- APP BODY --------------------
youtube_url = st.text_input("🎥 Enter YouTube URL")
transcript = None
audio_path = None

if st.button("Transcribe"):
    if youtube_url.strip() == "":
        st.error("Please enter a valid YouTube URL.")
    else:
        try:
            with st.spinner("🔊 Downloading audio..."):
                audio_path = download_audio(youtube_url)

            if os.path.exists(audio_path):
                st.audio(audio_path, format="audio/mp3")

                duration = get_audio_duration(audio_path)
                estimated_time = estimate_transcription_time(duration / 60)
                st.info(f"⏱ Estimated transcription time: {estimated_time} minutes")

                with st.spinner("📈 Rendering waveform..."):
                    fig = plot_waveform(audio_path)
                    st.pyplot(fig)

                with st.spinner("📝 Transcribing..."):
                    result = transcribe_audio(audio_path, language="en")
                    transcript = result["text"]

                    keywords = ["education", "science", "technology"]
                    highlighted_text = highlight_keywords(transcript, keywords)

                    st.markdown("### 🗣️ English Transcript")
                    st.markdown(highlighted_text)
            else:
                st.error(f"Audio file not found at {audio_path}")
        except Exception as e:
            st.error(f"Error: {e}")

# -------------------- PAYMENT SECTION --------------------
if transcript:
    st.markdown("""
    ### 💰 Transcript Access
    To download the transcript, please make a payment of ₹50 to the UPI ID below:

    **UPI ID:** `8146553307@yescred`  
    You may scan the QR code or use any UPI app to send payment.

    Once paid, upload a screenshot (optional) and click the confirmation button below.
    """)
    
    payment_proof = st.file_uploader("📸 Upload payment screenshot (optional)", type=["png", "jpg", "jpeg"])

    if st.button("✅ I've Paid – Unlock Transcript"):
        with open("transcript.pdf", "wb") as f:
            save_transcript_as_pdf(transcript)

        with open("transcript.pdf", "rb") as f:
            st.download_button(
                label="📥 Download English Transcript PDF",
                data=f.read(),
                file_name="transcript.pdf",
                mime="application/pdf"
            )
        st.success("Transcript is ready for download. Thank you for supporting!")

# -------------------- FOOTER --------------------
st.markdown("""
    <hr>
    <div style='text-align: center; font-size: 14px; padding-top: 10px;'>
        Made with ❤️ by <strong>Jagdev Singh Dosanjh</strong> |
        <a href='https://dosanjhpubsasr.org' target='_blank'>dosanjhpubsasr.org</a> |
        📧 <a href='mailto:jagdevsinghdosanjh@gmail.com'>jagdevsinghdosanjh@gmail.com</a> |
        📞 8146553307
    </div>
""", unsafe_allow_html=True)
