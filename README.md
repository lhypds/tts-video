TTS Video
=========


A simple tool to generate videos from text using TTS API.


Features
--------

- Convert text to speech using OpenAI's TTS API
- Automatic sentence splitting
- Generate numbered audio files (1.mp3, 2.mp3, 3.mp3, etc.)
- Combine audio files into one
- Create video with background image and combined audio
- Generate SRT subtitle files with accurate timing
- Multiple voice options: alloy, echo, fable, onyx, nova, shimmer
- Support for standard (tts-1) and HD quality (tts-1-hd) models


Quick Start
-----------

1. Run setup:
   ```bash
   ./setup.sh
   ```

2. Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

3. Edit `input.txt` with your text

4. Run:
   ```bash
   ./run.sh
   ```

5. Output

   All files are saved in the `output/` folder:
   - `1.mp3`, `2.mp3`, `3.mp3`, etc. - Individual sentence audio files
   - `audio.mp3` - Combined audio
   - `video.mp4` - Final video
   - `subtitles.srt` - Subtitle file with timing

