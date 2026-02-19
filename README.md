
TTS Video
=========

a simple tool to generate video from text, using TTS.

## Features

- Convert text to speech using OpenAI's TTS API
- **Automatic sentence splitting and SRT generation**
- **Simple numbered audio files** (1.mp3, 2.mp3, 3.mp3, etc.)
- Multiple voice options (alloy, echo, fable, onyx, nova, shimmer)
- Support for both standard (tts-1) and HD quality (tts-1-hd) models
- Automatic MP3 file generation with timestamps
- Generates subtitle files (SRT format) with accurate timing

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
   
   Edit `input.txt` with the text you want to convert to speech. You can include multiple sentences:
   ```
   你好，这是一个语音测试。这是第二句话。这是第三句话！
   ```

## Usage

Run the application:
```bash
./run.sh
```

The script will:
- Split your text into sentences
- Generate separate audio files for each sentence
- Name files simply as 1.mp3, 2.mp3, 3.mp3, etc.
- Create an SRT subtitle file (`input.srt`) with proper timing

Generated files:
- `output/1.mp3`, `output/2.mp3`, `output/3.mp3`, etc. - Audio files for each sentence
- `input.srt` - Subtitle file with timing information

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
│   ├── openai_utils.py    # OpenAI TTS utility functions
│   ├── audio_utils.py     # Audio duration and processing utilities
│   └── text_utils.py      # Text splitting and SRT generation
├── output/                 # Generated audio files (1.mp3, 2.mp3, etc.)
├── main.py                 # Main application script
├── input.txt              # Input text file
├── input.srt              # Generated subtitle file (SRT format)
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
```

## Customization

### Audio Files
Files are simply numbered:
- `1.mp3` - First sentence
- `2.mp3` - Second sentence
- `3.mp3` - Third sentence

### SRT File
Standard SRT format with millisecond precision:
```
1
00:00:00,000 --> 00:00:02,351
你好，这是一个语音测试

2
00:00:02,351 --> 00:00:03,527
这是第二句话
```

# Both options
text_to_speech("Your text here", voice="shimmer", model="tts-1-hd")
```

Available voices: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

## License

[Add your license here]
