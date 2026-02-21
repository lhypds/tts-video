#!/usr/bin/env python3
"""
Minimax Voice Clone Script

This script takes an MP3 file as input and creates a voice clone using Minimax's API.
It outputs a voice ID that can be used for text-to-speech synthesis.

Usage:
    python minimax_voice_clone.py <input_mp3_file> [--voice-id <custom_voice_id>]

Requirements:
    - Input MP3 file: 10 seconds to 5 minutes duration, up to 20 MB
    - MINIMAX_API_KEY must be set in environment variables or .env file

Example:
    python minimax_voice_clone.py samples/out.mp3 --voice-id my_custom_voice
"""

import os
import sys
import argparse
import warnings

# Suppress Python 3.13 hashlib warnings
warnings.filterwarnings('ignore', category=RuntimeWarning, module='hashlib')

import requests
from pathlib import Path
from dotenv import load_dotenv
import uuid


def upload_audio_file(file_path: str, api_key: str, purpose: str = "voice_clone") -> str:
    """
    Upload an audio file to Minimax and get a file_id.
    
    Args:
        file_path (str): Path to the audio file
        api_key (str): Minimax API key
        purpose (str): Purpose of the upload ("voice_clone" or "prompt_audio")
    
    Returns:
        str: The file_id returned by the API
    """
    url = "https://api.minimax.io/v1/files/upload"
    
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check file extension
    if file_path.suffix.lower() not in ['.mp3', '.m4a', '.wav']:
        raise ValueError(f"Unsupported file format: {file_path.suffix}. Supported: mp3, m4a, wav")
    
    # Check file size (20 MB limit)
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    if file_size_mb > 20:
        raise ValueError(f"File size {file_size_mb:.2f} MB exceeds 20 MB limit")
    
    payload = {"purpose": purpose}
    
    with open(file_path, "rb") as f:
        files = [("file", (file_path.name, f))]
        headers = {"Authorization": f"Bearer {api_key}"}
        
        print(f"Uploading {file_path.name} ({file_size_mb:.2f} MB)...")
        try:
            # Set timeout to 120 seconds for large files
            response = requests.post(url, headers=headers, data=payload, files=files, timeout=120)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise Exception("Upload timed out. Please check your network connection and try again.")
        except requests.exceptions.ConnectionError as e:
            raise Exception(f"Connection error during upload: {e}")
    
    result = response.json()
    file_id = result.get("file", {}).get("file_id")
    
    if not file_id:
        raise Exception(f"Failed to get file_id from response: {result}")
    
    print(f"✓ Upload successful! File ID: {file_id}")
    return file_id


def clone_voice(file_id: str, voice_id: str, api_key: str) -> str:
    """
    Clone a voice using the uploaded audio file.
    
    Args:
        file_id (str): The file_id of the uploaded audio
        voice_id (str): Custom voice ID to assign to this clone
        api_key (str): Minimax API key
    
    Returns:
        str: The voice_id of the cloned voice
    """
    url = "https://api.minimax.io/v1/voice_clone"
    
    payload = {
        "file_id": file_id,
        "voice_id": voice_id,
        "text": "This is a test of the cloned voice.",
        "model": "speech-2.8-hd"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"Cloning voice with ID: {voice_id}...")
    try:
        # Set timeout to 60 seconds
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise Exception("Voice cloning timed out. Please try again.")
    except requests.exceptions.ConnectionError as e:
        raise Exception(f"Connection error during cloning: {e}")
    
    result = response.json()
    print(f"✓ Voice clone successful!")
    
    # Optional: If the API returns extra audio data or metadata
    if "extra" in result:
        print(f"Response: {result.get('extra', {})}")
    
    return voice_id


def main():
    parser = argparse.ArgumentParser(
        description="Clone a voice from an MP3 file using Minimax API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python minimax_voice_clone.py samples/out.mp3
  python minimax_voice_clone.py samples/out.mp3 --voice-id my_custom_voice
  
Requirements:
  - Input file: MP3, M4A, or WAV format
  - Duration: 10 seconds to 5 minutes
  - File size: up to 20 MB
  - MINIMAX_API_KEY must be set in environment
        """
    )
    
    parser.add_argument(
        "input_file",
        help="Path to the input MP3/M4A/WAV file"
    )
    
    parser.add_argument(
        "--voice-id",
        help="Custom voice ID for the clone (if not provided, a UUID will be generated)",
        default=None
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("MINIMAX_API_KEY", "").strip().strip('"').strip("'")
    
    if not api_key:
        print("Error: MINIMAX_API_KEY not found in environment variables or .env file")
        sys.exit(1)
    
    # Generate voice ID if not provided
    if args.voice_id:
        voice_id = args.voice_id
    else:
        # Generate a unique voice ID using UUID
        voice_id = f"voice_{uuid.uuid4().hex[:12]}"
        print(f"Generated voice ID: {voice_id}")
    
    try:
        # Step 1: Upload the audio file
        file_id = upload_audio_file(args.input_file, api_key)
        
        # Step 2: Clone the voice
        result_voice_id = clone_voice(file_id, voice_id, api_key)
        
        # Output the voice ID
        print("\n" + "="*60)
        print(f"Voice ID: {result_voice_id}")
        print("="*60)
        print(f"\nYou can now use this voice ID in TTS calls:")
        print(f'  voice="{result_voice_id}"')
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        sys.exit(1)
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
