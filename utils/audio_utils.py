from mutagen.mp3 import MP3
import subprocess
import json


def get_audio_duration(file_path: str) -> float:
    """
    Get the duration of an audio file in seconds.
    
    Args:
        file_path (str): Path to the audio file
    
    Returns:
        float: Duration in seconds
    """
    try:
        # Try mutagen first
        audio = MP3(file_path)
        duration = audio.info.length
        
        # If mutagen returns 0 or None, try ffprobe as fallback
        if not duration or duration == 0:
            raise ValueError("Invalid duration from mutagen")
        
        return duration
    except Exception:
        # Fallback to ffprobe if mutagen fails
        try:
            result = subprocess.run(
                ['ffprobe', '-i', file_path, '-show_entries', 'format=duration', 
                 '-v', 'quiet', '-of', 'csv=p=0'],
                capture_output=True,
                text=True,
                check=True
            )
            return float(result.stdout.strip())
        except Exception as e:
            print(f"Warning: Could not determine duration for {file_path}: {e}")
            return 0.0
