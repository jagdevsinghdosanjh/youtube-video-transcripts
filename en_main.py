import streamlit as st
from matplotlib.figure import Figure
from datetime import datetime
import logging
from en_transcribe import transcribe_audio
from youtube_audio_downloader import download_audio, generate_job_id
from translator import get_supported_languages, translate_text, save_translated_pdf
from en_audio_tools import (
    get_audio_duration,
    estimate_transcription_time,
    plot_waveform,
    save_transcript_as_pdf,
    highlight_keywords,
)

logging.basicConfig(filename="error_log.txt", level=logging.ERROR)

# -------------------- UI COMPONENTS --------------------
def render_header():
    st.markdown(
        """
        <div style='text-align: center; padding: 10px 0;'>
            <h1 style='margin-bottom: 0;'>English YouTube Transcriber</h1>
            <p style='margin-top: 0; font-size: 16px;'>by <strong>Jagdev Singh Dosanjh</strong> | 
            <a href='https://dosanjhpubsasr.org' target='_blank'>dosanjhpubsasr.org</a> |
            📧 <a href='mailto:jagdevsinghdosanjh@gmail.com'>jagdevsinghdosanjh@gmail.com</a> |
            📞 8146553307</p>
            <hr>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_input():
    youtube_url = st.text_input("🎥 Enter YouTube URL", key="youtube_url_input")
    if st.button("Submit for Transcription", key="submit_button") and youtube_url:
        job_id = generate_job_id(youtube_url)
        st.session_state.job_queue.append({
            "id": job_id,
            "url": youtube_url,
            "status": "Queued",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transcript": None,
        })
        st.success(f"Job {job_id} added to queue.")

def render_footer():
    st.markdown(
        """
        <hr>
        <div style='text-align: center; font-size: 14px; padding-top: 10px;'>
            Made with ❤️ by <strong>Jagdev Singh Dosanjh</strong> |
            <a href='https://dosanjhpubsasr.org' target='_blank'>dosanjhpubsasr.org</a> |
            📧 <a href='mailto:jagdevsinghdosanjh@gmail.com'>jagdevsinghdosanjh@gmail.com</a> |
            📞 8146553307
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------- INIT --------------------
if "job_queue" not in st.session_state:
    st.session_state.job_queue = []

# -------------------- RENDER STATIC UI --------------------
render_header()
render_input()

# -------------------- PROCESS JOBS --------------------
for job in st.session_state.job_queue:
    if job["status"] == "Queued":
        job["status"] = "Processing"
        try:
            audio_path = download_audio(job["url"], job["id"])
            job["audio_path"] = audio_path

            duration = get_audio_duration(audio_path)
            job["duration"] = round(duration, 2)

            estimated_time = estimate_transcription_time(duration / 60)
            job["estimated_time"] = estimated_time

            st.markdown(f"#### 🎧 Waveform for Job {job['id']}")
            fig = plot_waveform(audio_path)
            if isinstance(fig, Figure):
                st.pyplot(fig)
            else:
                st.warning("Waveform could not be generated.")

            result = transcribe_audio(audio_path, language="en")
            job["transcript"] = result["text"]

            save_transcript_as_pdf(
                job["transcript"], filename=f"jobs/{job['id']}/transcript.pdf"
            )
            job["status"] = "Ready"
        except Exception as e:
            job["status"] = "Failed"
            logging.error(f"{datetime.now()} - Job {job['id']} failed: {str(e)}")
            st.error(f"Job {job['id']} failed: {str(e)}")

# -------------------- DISPLAY JOBS --------------------
st.markdown("### 📋 Transcription Queue")
for job in st.session_state.job_queue:
    st.markdown(f"- **{job['id']}** | {job['status']} | {job['timestamp']}")
    if job["status"] == "Ready":
        st.markdown("#### 🗣️ Transcript Preview")
        highlighted = highlight_keywords(
            job["transcript"], ["education", "science", "technology"]
        )
        st.markdown(highlighted)

        st.download_button(
            label="📥 Download Transcript PDF",
            data=open(f"jobs/{job['id']}/transcript.pdf", "rb").read(),
            file_name=f"{job['id']}_transcript.pdf",
            mime="application/pdf",
            key=f"download_{job['id']}",
        )

        language_options = get_supported_languages()
        target_lang = st.selectbox(
            "🌐 Choose translation language",
            options=list(language_options),
            index=list(language_options).index("english"),
            key=f"lang_select_{job['id']}"
        )

        if st.button("🌍 Translate Transcript", key=f"translate_button_{job['id']}"):
            try:
                translated_text = translate_text(job["transcript"], target_lang)
                st.markdown(f"### 🌍 Translated Transcript ({target_lang.title()})")
                st.markdown(translated_text)

                translated_pdf_path = f"jobs/{job['id']}/translated_{target_lang}.pdf"
                save_translated_pdf(translated_text, translated_pdf_path)

                with open(translated_pdf_path, "rb") as f:
                    st.download_button(
                        label=f"📥 Download {target_lang.title()} Transcript PDF",
                        data=f.read(),
                        file_name=f"{job['id']}_translated_{target_lang}.pdf",
                        mime="application/pdf",
                        key=f"translated_download_{job['id']}"
                    )
            except Exception as e:
                st.error(f"Translation failed: {str(e)}")

# -------------------- FOOTER --------------------
render_footer()
