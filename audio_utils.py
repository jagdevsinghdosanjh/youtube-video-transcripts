import librosa

def get_audio_duration(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    return librosa.get_duration(y=y, sr=sr)
