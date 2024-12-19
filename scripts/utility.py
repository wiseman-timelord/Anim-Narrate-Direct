# ./scripts/utility.py

import os
import yaml
from pathlib import Path
import psutil

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
    persistent_file: Path, 
    model_name: str, 
    speed: float, 
    pitch: float, 
    volume_gain: float, 
    threads_percent: int, 
    save_format: str
) -> tuple[dict, str]:
    """
    Save settings with validation and default handling.
    
    Args:
        persistent_file: Path to settings file
        model_name: Name of the TTS model
        speed: Speech speed multiplier (0.5-2.0)
        pitch: Voice pitch multiplier (0.5-2.0)
        volume_gain: Volume adjustment in dB (-20.0-20.0)
        threads_percent: CPU thread usage percentage (10-100)
        save_format: Audio format for saving (mp3/wav)
        
    Returns:
        tuple: (settings dict, status message)
    """
    try:
        # Validate inputs and apply defaults if necessary
        valid_formats = ["mp3", "wav"]
        save_format = save_format if save_format in valid_formats else "mp3"
        speed = max(0.5, min(speed, 2.0))
        pitch = max(0.5, min(pitch, 2.0))
        volume_gain = max(-20.0, min(volume_gain, 20.0))
        threads_percent = max(10, min(threads_percent, 100))

        settings = {
            "model_path": "./models",
            "voice_model": model_name,
            "speed": speed,
            "pitch": pitch,
            "volume_gain": volume_gain,
            "threads_percent": threads_percent,
            "save_format": save_format
        }

        # Ensure directory exists
        persistent_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write settings with backup
        backup_file = persistent_file.with_suffix('.yaml.bak')
        if persistent_file.exists():
            persistent_file.rename(backup_file)
            
        with open(persistent_file, 'w') as f:
            yaml.dump(settings, f)
            
        if backup_file.exists():
            backup_file.unlink()
            
        return settings, "Settings updated successfully!"
        
    except Exception as e:
        # Restore backup if available
        if 'backup_file' in locals() and backup_file.exists():
            backup_file.rename(persistent_file)
        return settings, f"Error saving settings: {str(e)}"

def detect_device():
    # Hardcode device to CPU
    device = "CPU"
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

def validate_and_set_default_model(settings, available_models, persistent_file, save_persistent_settings_func):
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
            settings["save_format"]
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
            settings["save_format"]
        )
        return updated_settings, True
    return settings, True

def get_system_resources():
    """
    Detects the number of CPU threads and available system RAM.
    """
    cpu_threads = psutil.cpu_count(logical=True)
    available_ram = psutil.virtual_memory().available / (1024 ** 3)  # Convert to GB
    return cpu_threads, available_ram

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
