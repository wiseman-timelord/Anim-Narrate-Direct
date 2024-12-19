# ./main_script.py

import os
from pathlib import Path
import torch
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
NVIDIA_DIR = Path("./venv/lib/python3.11/site-packages/nvidia")

GLOBAL_DEVICE = "cuda" if NVIDIA_DIR.exists() and torch.cuda.is_available() else "cpu"
print(f"Global device set to: {GLOBAL_DEVICE}")

# Load initial settings
settings = utility.load_persistent_settings(PERSISTENT_FILE)
device = utility.detect_device(NVIDIA_DIR)

available_models = utility.get_available_models(MODEL_DIR)
settings, _ = utility.validate_and_set_default_model(
    settings,
    available_models,
    PERSISTENT_FILE,
    utility.save_persistent_settings,
    lambda: utility.detect_device(NVIDIA_DIR)
)

if device == "CPU":
    tp = settings.get("threads_percent", 80)
    total_threads = os.cpu_count() or 1
    threads_to_set = max(1, int(total_threads * (tp / 100)))
    torch.set_num_threads(threads_to_set)
    threads_slider_initial_visible = True
else:
    threads_slider_initial_visible = False

default_model = settings["voice_model"] if settings["voice_model"] in available_models else (available_models[0] if available_models else "No models available")
initial_audio_status = "New Session"


# Handler functions (remain here to access globals)
def handle_generate_and_play(text, speaker_wav=None, language="en"):
    global CACHED_TEXT
    audio_status = "Generating Audio"
    audio_path = generate_tts_audio(
        text,
        settings["voice_model"],
        MODEL_DIR,
        GLOBAL_DEVICE,
        CACHED_TEXT,
        speaker_wav=speaker_wav,
        language=language
    )
    return "Audio Generated" if audio_path else "Error Generating Audio"


def handle_save_audio():
    global CACHED_TEXT  # Access the global variable
    if CACHED_TEXT["audio_path"]:
        saved_path = save_audio(CACHED_TEXT["audio_path"], settings["save_format"], settings["volume_gain"])
        if saved_path:
            return "Audio Saved"
        else:
            return "Error Saving Audio"
    else:
        return "No Audio To Save"


def handle_restart_session():
    print("Restarting session and reloading settings...")
    global settings, device, available_models

    # Reload settings
    settings = utility.load_persistent_settings(PERSISTENT_FILE)
    device = utility.detect_device(NVIDIA_DIR)
    available_models = utility.get_available_models(MODEL_DIR)

    if device == "CPU":
        tp = settings.get("threads_percent", 80)
        total_threads = os.cpu_count() or 1
        threads_to_set = max(1, int(total_threads * (tp / 100)))
        print(f"Setting number of threads to: {threads_to_set}")
        torch.set_num_threads(threads_to_set)
        visible = True
    else:
        visible = False

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
            settings["save_format"],
            lambda: utility.detect_device(NVIDIA_DIR)
        )

    print("Session restarted and settings reloaded.")
    return "Session Restarted and Settings Reloaded!", gr.update(visible=visible)


def handle_update_settings(model_name, speed, pitch, volume_gain, threads_percent, save_format):
    updated_settings, msg = utility.save_persistent_settings(
        PERSISTENT_FILE,
        model_name,
        speed,
        pitch,
        volume_gain,
        threads_percent,
        save_format,
        lambda: utility.detect_device(NVIDIA_DIR)
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
        threads_slider_initial_visible=threads_slider_initial_visible,
        handle_generate_and_play=handle_generate_and_play,
        handle_save_audio=handle_save_audio,
        handle_restart_session=handle_restart_session,
        exit_program=exit_program,  # Directly pass the function
        handle_update_settings=handle_update_settings
    )
    demo.launch(server_name="0.0.0.0", server_port=6942)


if __name__ == "__main__":
    main()
