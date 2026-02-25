TTS Video
=========


A simple tool to generate videos from text using TTS API.  
Support MiniMax and OpenAI's TTS API with multiple voice options and quality settings.  


Features
--------

- Convert text to speech.
- Automatic sentence splitting
- Generate SRT subtitle files with accurate timing
- Create video with background image


Quick Start
-----------

1. Run setup:
   ```bash
   ./setup.sh
   ```

2. Configure `.env`:

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


Voice Clone
-----------

You can also use MiniMax's voice cloning feature to create a custom voice.

1. Record a sample of your voice (or any voice you want to clone) and save it as `voice_sample.mp3` in the project root.

2. Run the voice cloning script:  
```bash
./clone_voice.sh voice_sample.mp3 --voice-id my_custom_voice
```

3. The cloned voice ID will be saved to `voice_id.txt`.
