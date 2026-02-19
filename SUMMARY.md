# TTS Video Project - Summary

## What Was Implemented

This project now automatically splits text into sentences and generates:
1. Individual audio files for each sentence with timeline-based naming
2. An SRT subtitle file with accurate timing

## Workflow

### Step 1: Prepare Input
Edit `input.txt` with your text. Multiple sentences are supported:
```
你好，这是一个语音测试。这是第二句话。这是第三句话！
```

### Step 2: Run the Script
```bash
./run.sh
# or
python main.py
```

### Step 3: Review Output

**Audio Files** (`output/` directory):
- `1.mp3` - First sentence
- `2.mp3` - Second sentence  
- `3.mp3` - Third sentence

**Subtitle File** (`input.srt`):
```srt
1
00:00:00,000 --> 00:00:02,351
你好，这是一个语音测试

2
00:00:02,351 --> 00:00:03,527
这是第二句话

3
00:00:03,527 --> 00:00:04,775
这是第三句话
```

## Features

✅ **Automatic Sentence Splitting**
- Handles Chinese and English punctuation (。！？.!?)
- Preserves sentence meaning and context

✅ **Timeline-Based File Naming**
- Files named with simple sequential numbers
- Easy to identify which audio corresponds to which sentence
- Format: `1.mp3`, `2.mp3`, `3.mp3`, etc.

✅ **SRT Subtitle Generation**
- Standard SubRip (SRT) format
- Millisecond precision timing
- Proper cumulative timing across all sentences
- UTF-8 encoding for international characters

✅ **Duration Tracking**
- Accurate audio duration measurement using mutagen
- Cumulative timing calculation
- Summary output with total duration

## Technical Details

### Dependencies
- `openai` - TTS API
- `mutagen` - Audio duration reading
- `python-dotenv` - Environment management

### File Structure
```
utils/
├── openai_utils.py   # OpenAI TTS integration
├── audio_utils.py    # Audio duration measurement
└── text_utils.py     # Text splitting and SRT formatting
```

### Key Functions

**Text Processing:**
- `split_into_sentences()` - Smart sentence splitting
- `format_srt_time()` - Convert seconds to SRT timestamp format
- `generate_srt_content()` - Create complete SRT file

**Audio Processing:**
- `get_audio_duration()` - Get MP3 duration in seconds
- `text_to_speech()` - Generate audio via OpenAI TTS

**Time Formatting:**
- `format_time()` - Convert seconds to H:MM:SS format (for filenames)
- `format_srt_time()` - Convert seconds to HH:MM:SS,mmm format (for SRT)

## Example Output

For the input: `"你好，这是一个语音测试。这是第二句话。这是第三句话！"`

**Console Output:**
```
Reading text from input.txt...
Text length: 26 characters
--------------------------------------------------
Found 3 sentence(s) to process:
  1. 你好，这是一个语音测试
  2. 这是第二句话
  3. 这是第三句话
--------------------------------------------------

Processing sentence 1/3...
✓ Generated: output/1.mp3
  Duration: 0:00:02
  
Processing sentence 2/3...
✓ Generated: output/2.mp3
  Duration: 0:00:01
  
Processing sentence 3/3...
✓ Generated: output/3.mp3
  Duration: 0:00:01

==================================================
Summary:
  Total sentences: 3
  Total audio files: 3
  Total duration: 0:00:04
  SRT file: input.srt
==================================================
```

## Next Steps (Potential Enhancements)

- [ ] Combine audio files into a single video
- [ ] Add background music
- [ ] Support for different audio formats
- [ ] Batch processing of multiple input files
- [ ] Custom sentence splitting rules
- [ ] GUI interface
- [ ] Video generation with subtitles
