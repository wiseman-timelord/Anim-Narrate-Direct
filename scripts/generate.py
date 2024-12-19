# ./scripts/generate.py

import os
import tempfile
import pyttsx3
from pydub import AudioSegment
import random
import string

def generate_tts_audio(text, model_name, model_dir, global_device, cached_text, speaker_wav=None, language="en"):
    """
    Generate TTS audio from text using pyttsx3.
    """
    try:
        output_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False, dir='./output').name

        # Initialize pyttsx3 engine
        engine = pyttsx3.init()

        # Set properties based on settings
        engine.setProperty('rate', 150)  # Example rate, adjust as needed
        engine.setProperty('volume', 1.0)  # Example volume, adjust as needed

        # Generate audio
        engine.save_to_file(text, output_path)
        engine.runAndWait()

        cached_text.update({"text": text, "audio_path": output_path})
        return output_path
    except Exception as e:
        print(f"Error during TTS generation: {e}")
        return None

def save_audio(audio_path, preferred_format, volume_gain):
    # save audio
    try:
        audio = AudioSegment.from_wav(audio_path)
        audio = audio + volume_gain
        random_hash = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        output_name = f"./output/{random_hash}.{preferred_format}"
        audio.export(output_name, format=preferred_format)
        return output_name
    except:
        return None
