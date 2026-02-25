#!/bin/bash

echo "Voice Cloning Script"
echo "===================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if input audio file is provided
if [ -z "$1" ]; then
    echo "Usage: ./clone_voice.sh <input_audio_file> [--voice-id <custom_voice_id>]"
    echo ""
    echo "Examples:"
    echo "  ./clone_voice.sh samples/out.mp3"
    echo "  ./clone_voice.sh samples/out.mp3 --voice-id my_custom_voice"
    echo ""
    echo "Requirements:"
    echo "  - Input file: MP3, M4A, or WAV format"
    echo "  - Duration: 10 seconds to 5 minutes"
    echo "  - File size: up to 20 MB"
    echo "  - MINIMAX_API_KEY must be set in .env file"
    exit 1
fi

# Check if input file exists
if [ ! -f "$1" ]; then
    echo "Error: Input file '$1' not found."
    exit 1
fi

# Run the voice cloning script with all arguments
echo "Cloning voice from: $1"
echo ""
python tools/minimax_voice_clone.py "$@"

echo ""
echo "===================="
echo "Voice cloning complete!"
