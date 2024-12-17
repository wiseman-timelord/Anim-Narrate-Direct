# Script: `./main_script.py`

import gradio as gr
import yaml, os
from pathlib import Path
import subprocess, tempfile, torch
from TTS.api import TTS
import hashlib, random, string

# Configuration and hardware file paths
PERSISTENT_FILE = Path("./data/persistent.yaml")
HARDWARE_FILE = Path("./data/hardware_details.txt")
MODEL_DIR = Path("./models")  # Default model directory
CACHED_TEXT = {"text": None, "audio_path": None}  # Cache for input text and generated audio

# Utility Functions
def load_persistent_settings():
    """
    Loads persistent settings from persistent.yaml.
    If the file doesn't exist, default settings are returned.
    """
    if not PERSISTENT_FILE.exists():
        default_settings = {
            "model_path": "./models",
            "voice_model": "default",
            "speed": 1.0,
            "pitch": 1.0,
            "volume_gain": 0.0,
            "session_history": "",
            "threads_percent": 80,
            "save_format": "mp3"
        }
        with open(PERSISTENT_FILE, 'w') as f:
            yaml.dump(default_settings, f)
        return default_settings
    else:
        with open(PERSISTENT_FILE, 'r') as f:
            return yaml.safe_load(f)


def save_persistent_settings(model_name, speed, pitch, save_format):
    """
    Saves updated settings to persistent.yaml.
    """
    settings = {
        "model_path": "./models",
        "voice_model": model_name,
        "speed": speed,
        "pitch": pitch,
        "volume_gain": 0.0,  # Default volume gain for now
        "session_history": "",
        "threads_percent": 80,
        "save_format": save_format
    }
    with open(PERSISTENT_FILE, 'w') as f:
        yaml.dump(settings, f)
    return "Settings updated successfully!"


def get_available_models():
    model_list = []
    for root, _, files in os.walk(MODEL_DIR):
        for file in files:
            if file.endswith(".pth"):
                relative_path = os.path.relpath(os.path.join(root, file), MODEL_DIR)
                model_list.append(relative_path)
    return model_list if model_list else ["No models available"]

def generate_tts_audio(text, model_name):
    # Check if the cached audio can be reused
    if CACHED_TEXT["text"] == text and CACHED_TEXT["audio_path"]:
        return CACHED_TEXT["audio_path"]

    # Generate new audio
    output_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False, dir='./output').name
    try:
        model_path = os.path.join(MODEL_DIR, model_name)
        print(f"Loading TTS model from '{model_path}'...")
        tts = TTS(model_path=model_path).to("cuda" if torch.cuda.is_available() else "cpu")
        tts.tts_to_file(text=text, file_path=output_path)
        CACHED_TEXT.update({"text": text, "audio_path": output_path})
        return output_path
    except Exception as e:
        print(f"Error generating TTS audio: {e}")
        return None

def save_audio(audio_path, preferred_format):
    random_hash = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    output_name = f"./output/{random_hash}.{preferred_format}"
    if preferred_format == "mp3":
        subprocess.run(["ffmpeg", "-y", "-i", audio_path, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", output_name], check=True)
    else:
        os.rename(audio_path, output_name)
    return output_name

# Load configurations
settings = load_persistent_settings()
available_models = get_available_models()
default_model = available_models[0] if available_models else "No models available"

# Gradio Interface
with gr.Blocks(title="Gen-Gradio-Voice") as demo:
    with gr.Tab("Narrator"):
        text_input = gr.Textbox(label="Enter Text", lines=3)
        model_selector = gr.Dropdown(label="Select TTS Model", choices=available_models, value=default_model)
        generate_button = gr.Button("Generate Speech")
        save_button = gr.Button("Save Narration")
        audio_output = gr.Audio(label="Output Audio", type="filepath")
        save_status = gr.Textbox(label="Save Status", interactive=False)

        # Generate and Play Immediately
        def generate_and_play(text, model_name):
            audio_path = generate_tts_audio(text, model_name)
            return audio_path

        generate_button.click(fn=generate_and_play, inputs=[text_input, model_selector], outputs=audio_output)

        # Save the audio in preferred format
        def save_audio_action():
            return save_audio(CACHED_TEXT["audio_path"], settings["save_format"])

        save_button.click(fn=save_audio_action, outputs=save_status)

    with gr.Tab("Configuration"):
        gr.Markdown("### Configuration Options")
        gr.Textbox(label="Available Models", value="\n".join(available_models), lines=5, interactive=False)
        speed_slider = gr.Slider(label="Speed", minimum=0.5, maximum=2.0, step=0.1, value=settings["speed"])
        pitch_slider = gr.Slider(label="Pitch", minimum=0.5, maximum=2.0, step=0.1, value=settings["pitch"])
        save_format_dropdown = gr.Dropdown(label="Preferred Save Format", choices=["mp3", "wav"], value=settings["save_format"])
        update_button = gr.Button("Update Settings")
        update_status = gr.Textbox(label="Update Status", interactive=False)

        update_button.click(
            fn=save_persistent_settings,
            inputs=[model_selector, speed_slider, pitch_slider, save_format_dropdown],
            outputs=update_status
        )

demo.launch(server_name="0.0.0.0", server_port=7860)

