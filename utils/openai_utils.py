import os
from pathlib import Path
from openai import OpenAI
from datetime import datetime


def text_to_speech(text: str, voice: str = "alloy", model: str = "tts-1") -> str:
    """
    Convert text to speech using OpenAI's TTS API and save as MP3 file.
    
    Args:
        text (str): The text to convert to speech
        voice (str): The voice to use. Options: alloy, echo, fable, onyx, nova, shimmer
        model (str): The TTS model to use. Options: tts-1, tts-1-hd
    
    Returns:
        str: Path to the generated MP3 file
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create result folder if it doesn't exist
    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_folder / f"speech_{timestamp}.mp3"
    
    # Generate speech
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    
    # Save to file
    response.stream_to_file(str(output_path))
    
    print(f"Audio saved to: {output_path}")
    return str(output_path)


if __name__ == "__main__":
    # Example usage
    sample_text = "Hello! This is a test of OpenAI's text to speech API."
    output_file = text_to_speech(sample_text)
    print(f"Generated audio file: {output_file}")
