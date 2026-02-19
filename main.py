from pathlib import Path
from utils.openai_utils import text_to_speech
from utils.audio_utils import get_audio_duration
from utils.text_utils import split_into_sentences, generate_srt_content
from utils.video_utils import combine_audio_files, create_video_with_audio
from dotenv import load_dotenv
from datetime import timedelta
import re


def format_time(seconds: float) -> str:
    """Convert seconds to H:MM:SS format"""
    td = timedelta(seconds=seconds)
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() % 3600) // 60)
    secs = int(td.total_seconds() % 60)
    return f"{hours}:{minutes:02d}:{secs:02d}"


def main():
    """
    Read text from input.txt, split into sentences, generate audio for each,
    and create an SRT file with proper timing.
    """
    # Load environment variables
    load_dotenv()
    
    # Define input file path
    input_file = Path("input.txt")
    srt_file = Path("output/subtitles.srt")
    
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
    
    # Split text into sentences
    sentences = split_into_sentences(text)
    
    if not sentences:
        print("No sentences found in the input text.")
        return
    
    print(f"Found {len(sentences)} sentence(s) to process:")
    for i, sentence in enumerate(sentences, 1):
        print(f"  {i}. {sentence}")
    print("-" * 50)
    
    # Generate audio for each sentence and track durations
    audio_files = []
    durations = []
    cumulative_time = 0
    
    try:
        for i, sentence in enumerate(sentences, 1):
            print(f"\nProcessing sentence {i}/{len(sentences)}...")
            print(f"Text: {sentence}")
            
            # Generate audio
            output_path = text_to_speech(sentence)
            
            # Get audio duration
            duration = get_audio_duration(output_path)
            durations.append(duration)
            
            # Rename file with simple number
            output_folder = Path("output")
            new_filename = f"{i}.mp3"
            new_path = output_folder / new_filename
            
            # Rename the file
            Path(output_path).rename(new_path)
            audio_files.append(new_path)
            
            print(f"✓ Generated: {new_path}")
            print(f"  Duration: {format_time(duration)}")
            
            cumulative_time += duration
        
        # Generate SRT file
        print("\n" + "=" * 50)
        print("Generating SRT file...")
        srt_content = generate_srt_content(sentences, durations)
        srt_file.write_text(srt_content, encoding='utf-8')
        
        print(f"✓ Created {srt_file}")
        
        # Combine audio files
        print("\n" + "=" * 50)
        print("Combining audio files...")
        audio_path = "output/audio.mp3"
        combine_audio_files(audio_files, audio_path)
        print(f"✓ Created {audio_path}")
        
        # Create video
        print("\nCreating video (200x600) with subtitles...")
        video_path = "output/video.mp4"
        create_video_with_audio(
            audio_path,
            video_path,
            srt_path=str(srt_file),
            width=200,
            height=600,
            bg_color=(0, 0, 0)  # Black background
        )
        print(f"✓ Created {video_path}")
        
        print("=" * 50)
        print(f"\nSummary:")
        print(f"  Total sentences: {len(sentences)}")
        print(f"  Total audio files: {len(audio_files)}")
        print(f"  Total duration: {format_time(cumulative_time)}")
        print(f"  SRT file: {srt_file}")
        print(f"  Combined audio: {audio_path}")
        print(f"  Video file: {video_path}")
        
    except Exception as e:
        print(f"Error generating audio: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
