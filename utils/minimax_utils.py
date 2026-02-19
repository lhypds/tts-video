import os
import asyncio
import websockets
import json
import ssl
from pathlib import Path
from datetime import datetime


def text_to_speech(text: str, output_filename: str = None, voice: str = "male-qn-qingse", model: str = "speech-2.8-hd") -> str:
    """
    Convert text to speech using Minimax's TTS API (WebSocket) and save as MP3 file.
    
    Args:
        text (str): The text to convert to speech
        voice (str): The voice ID to use. Common options:
                       - male-qn-qingse (青涩青年音色)
                       - male-qn-jingying (精英青年音色)
                       - male-qn-badao (霸道青年音色)
                       - male-qn-daxuesheng (青年大学生音色)
                       - female-shaonv (少女音色)
                       - female-yujie (御姐音色)
                       - female-chengshu (成熟女性音色)
                       - female-tianmei (甜美女性音色)
                       - presenter_male (男性主持人)
                       - presenter_female (女性主持人)
                       - audiobook_male_1 (男性有声书1)
                       - audiobook_male_2 (男性有声书2)
                       - audiobook_female_1 (女性有声书1)
                       - audiobook_female_2 (女性有声书2)
                       - English_expressive_narrator (English narrator)
        model (str): The TTS model to use. Options: speech-2.8-hd, speech-2.6-hd, 
                     speech-2.8-turbo, speech-2.6-turbo, speech-02-hd, speech-02-turbo
        output_filename (str): Custom filename for the output (optional). 
                              If not provided, uses timestamp. Can include .mp3 extension or not.
    
    Returns:
        str: Path to the generated MP3 file
    """
    # Get API credentials from environment
    api_key = os.getenv("MINIMAX_API_KEY", "").strip().strip('"').strip("'")
    group_id = os.getenv("MINIMAX_GROUP_ID", "").strip().strip('"').strip("'")
    
    if not api_key or not group_id:
        raise ValueError("MINIMAX_API_KEY and MINIMAX_GROUP_ID must be set in .env file")
    
    # Create output folder if it doesn't exist
    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)
    
    # Generate filename
    if output_filename:
        # Add .mp3 extension if not present
        if not output_filename.endswith('.mp3'):
            output_filename = f"{output_filename}.mp3"
        output_path = output_folder / output_filename
    else:
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_folder / f"speech_{timestamp}.mp3"
    
    # Run the async WebSocket communication
    try:
        asyncio.run(_text_to_speech_async(api_key, text, output_path, voice, model))
        print(f"Audio saved to: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"Error generating audio with Minimax: {e}")
        raise


async def _text_to_speech_async(api_key: str, text: str, output_path: Path, voice: str, model: str):
    """
    Async function to handle WebSocket communication with Minimax TTS API.
    """
    # WebSocket URL
    url = "wss://api.minimax.io/ws/v1/t2a_v2"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    audio_data = b""
    
    try:
        # Connect to WebSocket
        async with websockets.connect(url, additional_headers=headers, ssl=ssl_context) as websocket:
            # Wait for connection success
            connected = json.loads(await websocket.recv())
            if connected.get("event") != "connected_success":
                raise Exception(f"Connection failed: {connected}")
            
            # Start task
            start_msg = {
                "event": "task_start",
                "model": model,
                "voice_setting": {
                    "voice_id": voice,
                    "speed": 1.0,
                    "vol": 1.0,
                    "pitch": 0,
                    "english_normalization": False
                },
                "audio_setting": {
                    "sample_rate": 32000,
                    "bitrate": 128000,
                    "format": "mp3",
                    "channel": 1
                }
            }
            await websocket.send(json.dumps(start_msg))
            
            # Wait for task started
            response = json.loads(await websocket.recv())
            if response.get("event") != "task_started":
                raise Exception(f"Task start failed: {response}")
            
            # Send text for synthesis
            await websocket.send(json.dumps({
                "event": "task_continue",
                "text": text
            }))
            
            # Receive audio chunks
            chunk_counter = 0
            while True:
                response = json.loads(await websocket.recv())
                
                # Collect audio data
                if "data" in response and "audio" in response["data"]:
                    audio_hex = response["data"]["audio"]
                    if audio_hex:
                        audio_bytes = bytes.fromhex(audio_hex)
                        audio_data += audio_bytes
                        chunk_counter += 1
                
                # Check if synthesis is complete
                if response.get("is_final"):
                    break
            
            # Close task
            await websocket.send(json.dumps({"event": "task_finish"}))
            
    except Exception as e:
        raise Exception(f"WebSocket communication error: {e}")
    
    # Save audio to file
    if not audio_data:
        raise Exception("No audio data received from Minimax API")
    
    with open(output_path, 'wb') as f:
        f.write(audio_data)


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv
    load_dotenv()
    
    sample_text = "你好！这是Minimax语音合成API的测试。"
    output_file = text_to_speech(sample_text, voice="female-tianmei")
    print(f"Generated audio file: {output_file}")
