from moviepy import AudioFileClip, ColorClip, concatenate_audioclips
from pathlib import Path
from typing import List


def combine_audio_files(audio_files: List[str], output_path: str) -> str:
    """
    Combine multiple audio files into a single audio file.
    
    Args:
        audio_files (List[str]): List of audio file paths
        output_path (str): Path for the combined audio file
    
    Returns:
        str: Path to the combined audio file
    """
    audio_clips = [AudioFileClip(str(audio_file)) for audio_file in audio_files]
    audio = concatenate_audioclips(audio_clips)
    audio.write_audiofile(output_path)
    
    # Close clips to free resources
    for clip in audio_clips:
        clip.close()
    audio.close()
    
    return output_path


def create_video_with_audio(audio_path: str, output_path: str, width: int = 200, height: int = 600, 
                           bg_color: tuple = (0, 0, 0)) -> str:
    """
    Create a video with a solid color background and audio.
    
    Args:
        audio_path (str): Path to the audio file
        output_path (str): Path for the output video file
        width (int): Video width in pixels
        height (int): Video height in pixels
        bg_color (tuple): RGB color tuple for background (default: black)
    
    Returns:
        str: Path to the generated video file
    """
    # Load audio
    audio = AudioFileClip(audio_path)
    
    # Create a color clip (solid color video) with the same duration as audio
    video = ColorClip(size=(width, height), color=bg_color, duration=audio.duration)
    
    # Set the audio of the video clip
    video = video.with_audio(audio)
    
    # Write the video file
    video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )
    
    # Close clips to free resources
    video.close()
    audio.close()
    
    return output_path
