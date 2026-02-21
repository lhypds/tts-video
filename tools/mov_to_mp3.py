#!/usr/bin/env python3
"""
Convert .mov video files to .mp3 audio files using ffmpeg.

Usage:
    python mov_to_mp3.py input.mov [output.mp3]
    
If output filename is not provided, it will use the input filename with .mp3 extension.
"""

import sys
import os
import subprocess
from pathlib import Path


def convert_mov_to_mp3(input_file, output_file=None):
    """
    Convert a .mov file to .mp3 format.
    
    Args:
        input_file (str): Path to the input .mov file
        output_file (str, optional): Path to the output .mp3 file
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return False
    
    # Generate output filename if not provided
    if output_file is None:
        input_path = Path(input_file)
        output_file = str(input_path.with_suffix('.mp3'))
    
    # Ensure output has .mp3 extension
    if not output_file.endswith('.mp3'):
        output_file += '.mp3'
    
    print(f"Converting '{input_file}' to '{output_file}'...")
    
    try:
        # Run ffmpeg command to extract audio and convert to mp3
        # -i: input file
        # -vn: disable video recording
        # -acodec libmp3lame: use mp3 codec
        # -q:a 2: audio quality (0-9, lower is better, 2 is high quality ~170-210 kbps)
        # -y: overwrite output file if it exists
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vn',
            '-acodec', 'libmp3lame',
            '-q:a', '2',
            '-y',
            output_file
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✓ Successfully converted to '{output_file}'")
            
            # Display file size
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"  Output file size: {size_mb:.2f} MB")
            return True
        else:
            print(f"Error during conversion:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("Error: ffmpeg is not installed or not found in PATH.")
        print("Please install ffmpeg:")
        print("  macOS: brew install ffmpeg")
        print("  Linux: sudo apt-get install ffmpeg")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python mov_to_mp3.py input.mov [output.mp3]")
        print("\nExample:")
        print("  python mov_to_mp3.py video.mov")
        print("  python mov_to_mp3.py video.mov audio.mp3")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_mov_to_mp3(input_file, output_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
