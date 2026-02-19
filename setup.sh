#!/bin/bash

echo "Setting up TTS Video project..."
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "Python version: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p result

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    if [ -f ".env.exmaple" ]; then
        cp .env.exmaple .env
        echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
    else
        echo "OPENAI_API_KEY=your-api-key-here" > .env
        echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
    fi
else
    echo ".env file already exists."
fi

echo "================================"
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Edit input.txt with your text"
echo "3. Run: ./run.sh"
