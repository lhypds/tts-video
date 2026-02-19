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

# Remove subtitles.srt if it exists
if [ -f output/subtitles.srt ]; then
    echo "Removing subtitles.srt..."
    rm -f output/subtitles.srt
    echo "✓ Removed subtitles.srt"
else
    echo "No subtitles.srt file found"
fi

# Remove combined audio if it exists
if [ -f output/audio.mp3 ]; then
    echo "Removing audio.mp3..."
    rm -f output/audio.mp3
    echo "✓ Removed audio.mp3"
fi

# Remove video file if it exists
if [ -f output/video.mp4 ]; then
    echo "Removing video.mp4..."
    rm -f output/video.mp4
    echo "✓ Removed video.mp4"
fi

echo "=============================="
echo "Cleanup complete!"
