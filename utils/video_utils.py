from moviepy import AudioFileClip, ColorClip, concatenate_audioclips, TextClip, CompositeVideoClip
from pathlib import Path
from typing import List, Optional
import re


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


def parse_srt(srt_path: str) -> List[dict]:
    """
    Parse SRT file into a list of subtitle entries.
    
    Args:
        srt_path (str): Path to the SRT file
    
    Returns:
        List[dict]: List of subtitle dictionaries with start, end, and text
    """
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by double newlines to get each subtitle block
    blocks = content.strip().split('\n\n')
    subtitles = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            # Parse timestamp line (format: 00:00:00,000 --> 00:00:02,351)
            timestamp_line = lines[1]
            times = timestamp_line.split(' --> ')
            
            # Convert timestamp to seconds
            def timestamp_to_seconds(ts):
                h, m, s = ts.replace(',', '.').split(':')
                return int(h) * 3600 + int(m) * 60 + float(s)
            
            start = timestamp_to_seconds(times[0])
            end = timestamp_to_seconds(times[1])
            
            # Get subtitle text (can be multiple lines)
            text = '\n'.join(lines[2:])
            
            subtitles.append({
                'start': start,
                'end': end,
                'text': text
            })
    
    return subtitles


def create_video_with_audio(audio_path: str, output_path: str, srt_path: Optional[str] = None,
                           width: int = 200, height: int = 600, 
                           bg_color: tuple = (0, 0, 0)) -> str:
    """
    Create a video with a solid color background and audio, optionally with subtitles.
    
    Args:
        audio_path (str): Path to the audio file
        output_path (str): Path for the output video file
        srt_path (Optional[str]): Path to the SRT subtitle file (optional)
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
    
    # Add subtitles if SRT file is provided
    if srt_path and Path(srt_path).exists():
        subtitles = parse_srt(srt_path)
        subtitle_clips = []
        
        for sub in subtitles:
            # Create text clip for each subtitle
            # Try multiple fonts that support Chinese characters
            fonts_to_try = [
                '/System/Library/Fonts/STHeiti Medium.ttc',  # Full path to Chinese font
                '/System/Library/Fonts/PingFang.ttc',
                'Arial-Unicode-MS',
                'Arial'  # Fallback
            ]
            
            txt_clip = None
            for font_name in fonts_to_try:
                try:
                    txt_clip = TextClip(
                        text=sub['text'],
                        font=font_name,
                        font_size=24,
                        color='white',
                        text_align='center',
                        size=(width - 20, None),  # Width with padding
                        method='caption'
                    )
                    break  # Successfully created clip
                except (ValueError, OSError):
                    continue  # Try next font
            
            if txt_clip is None:
                # Last resort: use default font
                txt_clip = TextClip(
                    text=sub['text'],
                    font_size=24,
                    color='white',
                    text_align='center',
                    size=(width - 20, None),
                    method='caption'
                )
            
            # Set position (centered horizontally, bottom third of video)
            txt_clip = txt_clip.with_position(('center', height - 100))
            
            # Set timing
            txt_clip = txt_clip.with_start(sub['start']).with_duration(sub['end'] - sub['start'])
            
            subtitle_clips.append(txt_clip)
        
        # Composite video with subtitles
        if subtitle_clips:
            video = CompositeVideoClip([video] + subtitle_clips)
    
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
