#!/bin/bash

# Clean previous output first
./clean.sh

echo "Running TTS Video..."
echo "===================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run main.py
python main.py

echo "===================="
echo "Done!"
