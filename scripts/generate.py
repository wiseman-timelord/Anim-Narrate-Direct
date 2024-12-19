# ./scripts/generate.py

import os
import tempfile
import pyttsx3
from pydub import AudioSegment
import random
import string
import atexit

# Global to track temporary files
temp_files = set()

def cleanup_temp_files():
    """Clean up any temporary files on program exit"""
    for file_path in temp_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up temporary file {file_path}: {e}")

# Register cleanup function
atexit.register(cleanup_temp_files)

def generate_tts_audio(text, model_name, model_dir, cached_text, settings=None):
    """
    Generate TTS audio from text using pyttsx3.
    
    Args:
        text: Input text to convert to speech
        model_name: Name of the TTS model
        model_dir: Directory containing models
        cached_text: Dictionary to store cached text and audio path
        settings: Dictionary of TTS settings
        
    Returns:
        str: Path to generated audio file or None on failure
    """
    if not text or not isinstance(text, str):
        print("Error: Invalid input text")
        return None
        
    if settings is None:
        settings = {}
    
    engine = None
    output_path = None
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs('./output', exist_ok=True)
        
        # Create temporary file
        output_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False, dir='./output').name
        temp_files.add(output_path)

        # Initialize pyttsx3 engine
        engine = pyttsx3.init()

        # Validate and set properties
        speed = max(0.5, min(float(settings.get('speed', 1.0)), 2.0))
        volume = max(0.0, min(float(settings.get('volume', 1.0)), 1.0))

        engine.setProperty('rate', int(150 * speed))
        engine.setProperty('volume', volume)

        # Generate audio
        engine.save_to_file(text, output_path)
        engine.runAndWait()

        if not os.path.exists(output_path):
            raise FileNotFoundError("TTS engine failed to create audio file")
            
        # Verify file is not empty
        if os.path.getsize(output_path) == 0:
            raise ValueError("Generated audio file is empty")

        cached_text.update({"text": text, "audio_path": output_path})
        return output_path

    except Exception as e:
        print(f"Error during TTS generation: {e}")
        if engine:
            try:
                engine.stop()
            except:
                pass
                
        if output_path and os.path.exists(output_path):
            try:
                os.remove(output_path)
                temp_files.remove(output_path)
            except:
                pass
        return None
        
    finally:
        if engine:
            try:
                engine.stop()
            except:
                pass
def save_audio(audio_path, preferred_format, volume_gain):
    """
    Save audio with proper error handling and file management
    
    Args:
        audio_path: Path to input audio file
        preferred_format: Desired output format (mp3/wav)
        volume_gain: Volume adjustment in dB
        
    Returns:
        str: Path to saved audio file or None on failure
    """
    if not audio_path or not os.path.exists(audio_path):
        print("Error: Input audio file does not exist")
        return None
        
    if not preferred_format or preferred_format.lower() not in ['mp3', 'wav']:
        print("Error: Invalid output format specified")
        return None

    output_name = None
    try:
        # Load audio file
        audio = AudioSegment.from_wav(audio_path)
        
        # Apply volume adjustment
        try:
            volume_gain = float(volume_gain)
            volume_gain = max(-20.0, min(volume_gain, 20.0))
            audio = audio + volume_gain
        except ValueError:
            print("Warning: Invalid volume gain value, using original volume")

        # Create random hash for filename
        random_hash = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        output_name = f"./output/{random_hash}.{preferred_format.lower()}"
        
        # Ensure output directory exists
        os.makedirs("./output", exist_ok=True)
        
        # Export with proper error handling
        audio.export(output_name, format=preferred_format.lower())
        
        if not os.path.exists(output_name):
            raise FileNotFoundError("Failed to create output file")
            
        # Verify file is not empty
        if os.path.getsize(output_name) == 0:
            raise ValueError("Generated output file is empty")
            
        return output_name

    except Exception as e:
        print(f"Error saving audio: {e}")
        if output_name and os.path.exists(output_name):
            try:
                os.remove(output_name)
            except:
                pass
        return None
