from pathlib import Path
from utils.openai_utils import text_to_speech
from dotenv import load_dotenv


def main():
    """
    Read text from input.txt and generate audio using OpenAI TTS.
    """
    # Load environment variables
    load_dotenv()
    
    # Define input file path
    input_file = Path("input.txt")
    
    # Create input.txt if it doesn't exist
    if not input_file.exists():
        print(f"Creating {input_file}...")
        input_file.write_text("Hello! This is a sample text for text-to-speech conversion.")
        print(f"Please edit {input_file} with your desired text and run again.")
        return
    
    # Read text from input.txt
    text = input_file.read_text().strip()
    
    if not text:
        print(f"Error: {input_file} is empty. Please add some text.")
        return
    
    print(f"Reading text from {input_file}...")
    print(f"Text length: {len(text)} characters")
    print("-" * 50)
    
    # Generate audio
    try:
        output_path = text_to_speech(text)
        print("-" * 50)
        print(f"✓ Audio file generated successfully: {output_path}")
    except Exception as e:
        print(f"Error generating audio: {e}")


if __name__ == "__main__":
    main()
