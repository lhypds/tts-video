#!/bin/bash

# Cleanup script to remove generated audio files and SRT file

echo "Cleaning up generated files..."
echo "=============================="

# Remove all MP3 files from output directory
mp3_count=$(ls output/*.mp3 2>/dev/null | wc -l)
if [ "$mp3_count" -gt 0 ]; then
    echo "Removing $mp3_count MP3 file(s) from output/..."
    rm -f output/*.mp3
    echo "✓ Removed all MP3 files"
else
    echo "No MP3 files found in output/"
fi

# Remove input.srt if it exists
if [ -f input.srt ]; then
    echo "Removing input.srt..."
    rm -f input.srt
    echo "✓ Removed input.srt"
else
    echo "No input.srt file found"
fi

echo "=============================="
echo "Cleanup complete!"
