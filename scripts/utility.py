# ./scripts/utility.py

import os
import yaml
from pathlib import Path

def load_persistent_settings(persistent_file):
    # load settings
    if not persistent_file.exists():
        default_settings = {
            "model_path": "./models",
            "voice_model": "default",
            "speed": 1.0,
            "pitch": 1.0,
            "volume_gain": 0.0,
            "threads_percent": 80,
            "save_format": "mp3"
        }
        with open(persistent_file, 'w') as f:
            yaml.dump(default_settings, f)
        return default_settings
    else:
        with open(persistent_file, 'r') as f:
            return yaml.safe_load(f)


def save_persistent_settings(
    persistent_file, 
    model_name, 
    speed, 
    pitch, 
    volume_gain, 
    threads_percent, 
    save_format, 
    detect_device_func
):
    """
    Save settings with validation and default handling.
    """
    device = detect_device_func()

    # Validate inputs and apply defaults if necessary
    valid_formats = ["mp3", "wav"]
    save_format = save_format if save_format in valid_formats else "mp3"
    speed = speed if 0.5 <= speed <= 2.0 else 1.0
    pitch = pitch if 0.5 <= pitch <= 2.0 else 1.0
    volume_gain = max(-20.0, min(volume_gain, 20.0))
    threads_percent = threads_percent if 10 <= threads_percent <= 100 else 80

    settings = {
        "model_path": "./models",
        "voice_model": model_name,
        "speed": speed,
        "pitch": pitch,
        "volume_gain": volume_gain,
        "threads_percent": threads_percent if device == "CPU" else 80,
        "save_format": save_format
    }

    with open(persistent_file, 'w') as f:
        yaml.dump(settings, f)
    return settings, "Settings updated successfully!"


def detect_device(nvidia_dir):
    # detect device
    print("Detecting device...")
    device_is_gpu = (nvidia_dir.exists() and torch.cuda.is_available())
    device = "GPU" if device_is_gpu else "CPU"
    print(f"Device detected: {device}")
    return device


def get_available_models(model_dir):
    """
    Detects all available models in the models directory.
    """
    model_list = []
    for root, _, files in os.walk(model_dir):
        for file in files:
            if file.endswith(".pth"):
                relative_path = os.path.relpath(os.path.join(root, file), model_dir)
                model_list.append(relative_path)
    return model_list


def validate_and_set_default_model(settings, available_models, persistent_file, save_persistent_settings_func, detect_device_func):
    """
    Ensures a valid model is selected. If not, sets a placeholder.
    """
    if not available_models:
        print("Error: No valid models found in the './models' directory.")
        settings["voice_model"] = "No models available"
        _, msg = save_persistent_settings_func(
            persistent_file,
            settings["voice_model"],
            settings["speed"],
            settings["pitch"],
            settings["volume_gain"],
            settings["threads_percent"],
            settings["save_format"],
            detect_device_func
        )
        return settings, False

    if settings["voice_model"] not in available_models:
        print(f"Default model '{settings['voice_model']}' not found. Selecting the first available model.")
        
        # Print the model folder that contains the .pth file
        if available_models:
            selected_model_folder = available_models[0].split("/")[0]  # Extract the folder name
            print(f"Selected model folder: {selected_model_folder}")
        
        settings["voice_model"] = available_models[0]
        updated_settings, msg = save_persistent_settings_func(
            persistent_file,
            settings["voice_model"],
            settings["speed"],
            settings["pitch"],
            settings["volume_gain"],
            settings["threads_percent"],
            settings["save_format"],
            detect_device_func
        )
        return updated_settings, True
    return settings, True


def exit_program():
    """
    Gracefully exit the program:
    - Stops the Gradio server.
    - Executes any cleanup functions.
    - Exits the Python script cleanly, returning to bash.
    """
    print("Shutting down Gradio server and cleaning up resources...")

    # Cleanup resources if necessary
    try:
        # Add any additional cleanup logic here
        print("Performing cleanup tasks...")
    except Exception as e:
        print(f"Error during cleanup: {e}")

    # Terminate the Python script
    print("Exiting program...")
    os._exit(0)
