import streamlit as st
import os
from transcribe import transcribe_audio
from youtube_audio_downloader import download_audio
from audio_tools import (
    get_audio_duration,
    estimate_transcription_time,
    plot_waveform,
    highlight_keywords,
    save_transcript_as_pdf,
    to_gurmukhi
)

st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <h1 style='margin-bottom: 0;'>Punjabi YouTube Transcriber</h1>
        <p style='margin-top: 0; font-size: 16px;'>by <strong>Jagdev Singh Dosanjh</strong> | 
        <a href='https://dosanjhpubsasr.org' target='_blank'>dosanjhpubsasr.org</a> |
        📧 <a href='mailto:jagdevsinghdosanjh@gmail.com'>jagdevsinghdosanjh@gmail.com</a> |
        📞 8146553307</p>
        <hr>
    </div>
""", unsafe_allow_html=True)

youtube_url = st.text_input("🎥 Enter YouTube URL")
transcript = None
gurmukhi_text = None
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
                    result = transcribe_audio(audio_path)
                    transcript = result["text"]
                    gurmukhi_text = to_gurmukhi(transcript)

                    keywords = ["ਪਿਆਰ", "ਸੱਚ", "ਜੀਵਨ"]
                    highlighted_text = highlight_keywords(gurmukhi_text, keywords)

                    st.markdown("### 🗣️ Gurmukhi Transcript")
                    st.markdown(highlighted_text)
            else:
                st.error(f"Audio file not found at {audio_path}")
        except Exception as e:
            st.error(f"Error: {e}")

# Show download button only if Gurmukhi transcript exists
if gurmukhi_text:
    if st.button("📥 Download Gurmukhi Transcript as PDF"):
        save_transcript_as_pdf(gurmukhi_text)
        st.success("Transcript saved as transcript.pdf")

st.markdown("""
    <hr>
    <div style='text-align: center; font-size: 14px; padding-top: 10px;'>
        Made with ❤️ by <strong>Jagdev Singh Dosanjh</strong> |
        <a href='https://dosanjhpubsasr.org' target='_blank'>dosanjhpubsasr.org</a> |
        📧 <a href='mailto:jagdevsinghdosanjh@gmail.com'>jagdevsinghdosanjh@gmail.com</a> |
        📞 8146553307
    </div>
""", unsafe_allow_html=True)
