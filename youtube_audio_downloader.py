# youtube_audio_downloader.py

import yt_dlp
import os
import hashlib
import time

def generate_job_id(youtube_url: str) -> str:
    """Generates a unique job ID based on URL hash and timestamp."""
    timestamp = int(time.time())
    url_hash = hashlib.md5(youtube_url.encode()).hexdigest()[:6]
    return f"{url_hash}_{timestamp}"

def download_audio(youtube_url: str, job_id: str) -> str:
    """Downloads audio from YouTube and saves it under a unique job folder."""
    job_folder = os.path.join("jobs", job_id)
    os.makedirs(job_folder, exist_ok=True)

    output_template = os.path.join(job_folder, "audio.webm")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return output_template.replace(".webm", ".mp3")
