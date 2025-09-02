import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import torch
from fpdf import FPDF

def plot_waveform(audio_path: str) -> Figure:
    y, sr = librosa.load(audio_path, sr=None)
    fig, ax = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y, sr=sr, alpha=0.6, ax=ax)
    ax.set_title("Audio Waveform")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    fig.tight_layout()
    return fig

def get_audio_duration(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    return librosa.get_duration(y=y, sr=sr)

def estimate_transcription_time(duration_minutes, device=None):
    if device is None:
        device = "gpu" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        return round(duration_minutes * 1.2)
    elif device == "gpu":
        return round(duration_minutes * 0.3)
    return round(duration_minutes)

def save_transcript_as_pdf(text, filename="transcript.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)

def highlight_keywords(text, keywords):
    for word in keywords:
        text = text.replace(word, f"**:blue[{word}]**")
    return text
