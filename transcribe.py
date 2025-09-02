import whisper
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


model = whisper.load_model("base")

def transcribe_audio(file_path: str, language: str = "pa") -> dict:
    """
    Transcribes the given audio file using Whisper.

    Args:
        file_path (str): Path to the audio file.
        language (str): Language code (default is Punjabi 'pa').

    Returns:
        dict: Transcription result.
    """
    return model.transcribe(file_path, language=language)

# import whisper

# model = whisper.load_model("base")
# result = model.transcribe("audio.mp3", language="pa")
# print(result["text"])
