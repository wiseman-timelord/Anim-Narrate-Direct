# ./main_script.py

import os
from pathlib import Path
import yaml

# Import utilities and interface
from scripts import utility
from scripts.utility import exit_program
from scripts.interface import create_interface
from scripts.generate import generate_tts_audio, save_audio

# Globals
CACHED_TEXT = {"text": None, "audio_path": None}  # Ensure this global is defined
PERSISTENT_FILE = Path("./data/persistent.yaml")
MODEL_DIR = Path("./models")
OUTPUT_DIR = Path("./output")

# Load initial settings
settings = utility.load_persistent_settings(PERSISTENT_FILE)

available_models = utility.get_available_models(MODEL_DIR)
settings, _ = utility.validate_and_set_default_model(
    settings,
    available_models,
    PERSISTENT_FILE,
    utility.save_persistent_settings
)

default_model = settings["voice_model"] if settings["voice_model"] in available_models else (available_models[0] if available_models else "No models available")
initial_audio_status = "New Session"

# Handler functions (remain here to access globals)
def handle_generate_and_play(text):
    global CACHED_TEXT, settings
    
    if not text or not isinstance(text, str):
        return "Error: Invalid text input"
    
    if len(text.strip()) == 0:
        return "Error: Empty text input"
    
    try:
        audio_status = "Generating Audio..."
        
        # Validate settings
        if not settings or not isinstance(settings, dict):
            print("Error: Invalid settings configuration")
            return "Error: Invalid configuration"
            
        if "voice_model" not in settings:
            print("Error: No voice model configured")
            return "Error: No voice model available"
        
        audio_path = generate_tts_audio(
            text,
            settings["voice_model"],
            MODEL_DIR,
            CACHED_TEXT,
            settings
        )
        
        if not audio_path:
            return "Error: Failed to generate audio"
            
        if not os.path.exists(audio_path):
            return "Error: Generated audio file not found"
            
        # Verify file is not empty
        if os.path.getsize(audio_path) == 0:
            return "Error: Generated audio file is empty"
            
        return "Audio Generated Successfully"
        
    except Exception as e:
        print(f"Error in handle_generate_and_play: {e}")
        return f"Error: Failed to generate audio - {str(e)}"

def handle_save_audio():
    global CACHED_TEXT
    
    if not CACHED_TEXT:
        return "Error: No cached audio data"
        
    if not CACHED_TEXT.get("audio_path"):
        return "Error: No audio file to save"
        
    if not os.path.exists(CACHED_TEXT["audio_path"]):
        return "Error: Cached audio file not found"
        
    try:
        saved_path = save_audio(
            CACHED_TEXT["audio_path"],
            settings.get("save_format", "mp3"),
            settings.get("volume_gain", 0.0)
        )
        
        if not saved_path:
            return "Error: Failed to save audio"
            
        if not os.path.exists(saved_path):
            return "Error: Saved audio file not found"
            
        return f"Audio saved successfully: {os.path.basename(saved_path)}"
        
    except Exception as e:
        print(f"Error in handle_save_audio: {e}")
        return f"Error: Failed to save audio - {str(e)}"

def handle_restart_session():
    print("Restarting session and reloading settings...")
    global settings, available_models

    # Reload settings
    settings = utility.load_persistent_settings(PERSISTENT_FILE)
    available_models = utility.get_available_models(MODEL_DIR)

    if settings["voice_model"] not in available_models:
        print(f"Current voice_model '{settings['voice_model']}' not found in available models. Updating settings.")
        if available_models and available_models[0] != "No models available":
            settings["voice_model"] = available_models[0]
        else:
            settings["voice_model"] = "No models available"

        settings, _ = utility.save_persistent_settings(
            PERSISTENT_FILE,
            settings["voice_model"],
            settings["speed"],
            settings["pitch"],
            settings["volume_gain"],
            settings["threads_percent"],
            settings["save_format"]
        )

    print("Session restarted and settings reloaded.")
    return "Session Restarted and Settings Reloaded!"

def handle_update_settings(model_name, speed, pitch, volume_gain, threads_percent, save_format):
    updated_settings, msg = utility.save_persistent_settings(
        PERSISTENT_FILE,
        model_name,
        speed,
        pitch,
        volume_gain,
        threads_percent,
        save_format
    )
    # Update global settings after saving
    global settings
    settings = updated_settings
    return msg

def main():
    demo = create_interface(
        available_models=available_models,
        default_model=default_model,
        initial_audio_status=initial_audio_status,
        settings=settings,
        handle_generate_and_play=handle_generate_and_play,
        handle_save_audio=handle_save_audio,
        handle_restart_session=handle_restart_session,
        exit_program=exit_program,  # Directly pass the function
        handle_update_settings=handle_update_settings
    )
    demo.launch(server_name="0.0.0.0", server_port=6942)

if __name__ == "__main__":
    main()
