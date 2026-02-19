import re
from typing import List


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences based on common punctuation marks.
    Handles Chinese and English text.
    
    Args:
        text (str): The text to split
    
    Returns:
        List[str]: List of sentences
    """
    # Split by common sentence-ending punctuation
    # Handles: . ! ? 。 ！ ？ and newlines
    sentences = re.split(r'[.!?。！？\n]+', text)
    
    # Clean up and filter empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences


def format_srt_time(seconds: float) -> str:
    """
    Convert seconds to SRT timestamp format: HH:MM:SS,mmm
    
    Args:
        seconds (float): Time in seconds
    
    Returns:
        str: Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def create_srt_entry(index: int, start_time: float, end_time: float, text: str) -> str:
    """
    Create a single SRT entry.
    
    Args:
        index (int): Subtitle index (starting from 1)
        start_time (float): Start time in seconds
        end_time (float): End time in seconds
        text (str): The subtitle text
    
    Returns:
        str: Formatted SRT entry
    """
    start = format_srt_time(start_time)
    end = format_srt_time(end_time)
    
    return f"{index}\n{start} --> {end}\n{text}\n"


def generate_srt_content(sentences: List[str], durations: List[float]) -> str:
    """
    Generate complete SRT content from sentences and their durations.
    
    Args:
        sentences (List[str]): List of sentences
        durations (List[float]): List of durations for each sentence
    
    Returns:
        str: Complete SRT file content
    """
    if len(sentences) != len(durations):
        raise ValueError("Number of sentences must match number of durations")
    
    srt_content = ""
    cumulative_time = 0.0
    
    for i, (sentence, duration) in enumerate(zip(sentences, durations), 1):
        start_time = cumulative_time
        end_time = cumulative_time + duration
        
        srt_content += create_srt_entry(i, start_time, end_time, sentence)
        srt_content += "\n"
        
        cumulative_time = end_time
    
    return srt_content.strip()
