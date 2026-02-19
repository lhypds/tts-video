
TTS Video
=========

a simple tool to generate video from text, using TTS.

## Features

- Convert text to speech using OpenAI's TTS API
- Multiple voice options (alloy, echo, fable, onyx, nova, shimmer)
- Support for both standard (tts-1) and HD quality (tts-1-hd) models
- Automatic MP3 file generation with timestamps

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd tts-video
   ```

2. **Run the setup script**:
   ```bash
   ./setup.sh
   ```
   
   This will:
   - Create a virtual environment
   - Install all required dependencies
   - Create necessary directories
   - Generate a `.env` file

3. **Configure your API key**:
   
   Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

4. **Prepare your text**:
   
   Edit `input.txt` with the text you want to convert to speech.

## Usage

Run the application:
```bash
./run.sh
```

The generated MP3 file will be saved in the `output/` folder with a timestamp.

## Manual Usage

If you prefer to run without the scripts:

1. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Run the main script**:
   ```bash
   python main.py
   ```

## Project Structure

```
tts-video/
├── utils/
│   └── openai_utils.py    # OpenAI TTS utility functions
├── output/                 # Generated audio files
├── main.py                 # Main application script
├── input.txt              # Input text file
├── setup.sh               # Setup script
├── run.sh                 # Run script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
└── README.md             # This file
```

## Customization

You can customize the voice and model in your code:

```python
from utils.openai_utils import text_to_speech

# Use a different voice
text_to_speech("Your text here", voice="nova")

# Use HD quality
text_to_speech("Your text here", model="tts-1-hd")

# Both options
text_to_speech("Your text here", voice="shimmer", model="tts-1-hd")
```

Available voices: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

## License

[Add your license here]
