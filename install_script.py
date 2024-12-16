# Script: `./install_script.py`

import os
import subprocess
from pathlib import Path
import json
import urllib.request
import zipfile

# Constants
PERSISTENT_FILE = Path("./data/persistent.json")
VENV_PATH = Path("./venv")
REQUIREMENTS_FILE = Path("./data/requirements.txt")
HARDWARE_FILE = Path("./data/hardware_details.txt")
FOLDERS_TO_CREATE = ["./models", "./output", "./data"]

def check_sudo():
    if os.geteuid() != 0:
        print("Error: Sudo Authorization Required!")
        exit(1)
    print("Sudo authorization confirmed.")

def create_folders():
    results = {}
    for folder in FOLDERS_TO_CREATE:
        path = Path(folder)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            path.chmod(0o777)  # Ensure all created folders have 777 permissions
            results[folder] = "Created"
        else:
            results[folder] = "Already exists"
    return results

def create_data_init_py():
    init_file = Path("./data/__init__.py")
    init_file.write_text("# This file marks this directory as a Python package.\n")
    init_file.chmod(0o777)
    return "Initialization file created."

def create_data_requirements():
    requirements = """gradio
transformers
torch
pydub
ffmpeg-python
huggingface_hub
PyYAML
"""
    REQUIREMENTS_FILE.write_text(requirements)
    REQUIREMENTS_FILE.chmod(0o777)
    return "Requirements file created."

def create_hardware_details():
    cpu_name = subprocess.getoutput("grep -m 1 'model name' /proc/cpuinfo | awk -F: '{print $2}'").strip()
    cpu_threads = subprocess.getoutput('lscpu | grep "^CPU(s):" | awk "{print $2}"').strip()
    system_ram = subprocess.getoutput('free -h | grep "Mem:" | awk "{print $2}"').strip()
    os_info = subprocess.getoutput('uname -a').strip()
    hardware_info = [f"CPU Name: {cpu_name}", f"CPU Threads Total: {cpu_threads}", f"Total System RAM: {system_ram}", f"OS Info: {os_info}"]
    HARDWARE_FILE.write_text("\n".join(hardware_info))
    HARDWARE_FILE.chmod(0o777)
    return "Hardware details saved."

def create_persistent_json():
    persistent_content = {"voice_model": "default", "speed": 1.0, "pitch": 1.0, "volume_gain": 0.0, "session_history": "", "threads_percent": 80, "model_path": "./models"}
    with open(PERSISTENT_FILE, 'w') as f:
        json.dump(persistent_content, f, indent=4)
    PERSISTENT_FILE.chmod(0o777)
    return "Persistent settings saved."

def download_and_install_tts():
    url = "https://github.com/coqui-ai/TTS/archive/refs/tags/v0.22.0.zip"
    local_zip_path = Path("./TTS.zip")
    urllib.request.urlretrieve(url, local_zip_path)
    with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
        zip_ref.extractall("./")
    install_dir = "./TTS-0.22.0"
    subprocess.run([str(VENV_PATH / "bin/python3"), "-m", "pip", "install", "-e", install_dir])
    local_zip_path.unlink()  # Remove the downloaded zip file
    return f"TTS installed from {install_dir}"

def install_requirements():
    """
    Installs Python dependencies and GPU or CPU-specific libraries based on system configuration.
    """
    try:
        subprocess.run([str(VENV_PATH / "bin/python3"), "-m", "pip", "install", "--upgrade", "pip"], check=True)

        if subprocess.getoutput("command -v nvidia-smi"):
            print("GPU detected. Installing GPU-based dependencies...")
            subprocess.run([
                str(VENV_PATH / "bin/python3"), "-m", "pip", "install",
                "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu117"
            ], check=True)
        else:
            print("No GPU detected. Installing CPU-based dependencies...")
            subprocess.run([
                str(VENV_PATH / "bin/python3"), "-m", "pip", "install",
                "torch", "torchvision", "torchaudio"
            ], check=True)

        subprocess.run([str(VENV_PATH / "bin/python3"), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)], check=True)
        print("Python libraries installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        return download_and_install_tts()  # Fallback to direct installation.

def create_virtualenv():
    if not VENV_PATH.exists():
        subprocess.run(["python3", "-m", "venv", str(VENV_PATH)], check=True)
        VENV_PATH.chmod(0o777)
        return "Virtual environment created and permissions set to 777."
    else:
        return "Virtual environment already exists."

def main():
    print(check_sudo())
    print(create_folders())
    print(create_data_init_py())
    print(create_data_requirements())
    print(create_virtualenv())
    print(install_requirements())
    print(create_hardware_details())
    print(create_persistent_json())

if __name__ == "__main__":
    main()

