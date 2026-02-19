from mutagen.mp3 import MP3


def get_audio_duration(file_path: str) -> float:
    """
    Get the duration of an audio file in seconds.
    
    Args:
        file_path (str): Path to the audio file
    
    Returns:
        float: Duration in seconds
    """
    audio = MP3(file_path)
    return audio.info.length
