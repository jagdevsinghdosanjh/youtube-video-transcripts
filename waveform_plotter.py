# waveform_plotter.py
import librosa
import matplotlib.pyplot as plt
import numpy as np # noqa

def plot_waveform(audio_path: str):
    y, sr = librosa.load(audio_path, sr=None)
    plt.figure(figsize=(10, 3))
    librosa.display.waveshow(y, sr=sr, alpha=0.6)
    plt.title("Audio Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    return plt
