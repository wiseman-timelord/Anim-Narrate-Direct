# Script: `./install_script.py`

import os, re, subprocess
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
    """
    Creates necessary project directories with 777 permissions.
    """
    results = {}
    for folder in FOLDERS_TO_CREATE:
        path = Path(folder)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            path.chmod(0o777)
            results[folder] = "Created"
        else:
            results[folder] = "Already exists"

        # Ensure all files and subdirectories inside have 777 permissions
        for root, dirs, files in os.walk(folder):
            for dir_ in dirs:
                Path(os.path.join(root, dir_)).chmod(0o777)
            for file_ in files:
                Path(os.path.join(root, file_)).chmod(0o777)

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
TTS
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


def install_requirements():
    """
    Installs required Python dependencies from requirements.txt.
    Handles GPU-optimized installations of PyTorch if CUDA is detected.
    """
    try:
        print("Upgrading pip...")
        subprocess.run([
            str(VENV_PATH / "bin/python3"), "-m", "pip", "install", "--upgrade", "pip"
        ], check=True)

        # Detect CUDA version for GPU dependencies
        cuda_version_output = subprocess.getoutput("nvcc --version")
        if "release" in cuda_version_output:
            cuda_version = re.search(r"release (\d+\.\d+)", cuda_version_output).group(1)
            cuda_tag = "cu" + cuda_version.replace(".", "")
            torch_wheel_index = f"https://download.pytorch.org/whl/{cuda_tag}/"
            print(f"GPU detected with CUDA {cuda_version}. Installing GPU-optimized PyTorch...")
            subprocess.run([
                str(VENV_PATH / "bin/python3"), "-m", "pip", "install",
                "torch", "torchvision", "torchaudio", "--extra-index-url", torch_wheel_index
            ], check=True)
        else:
            print("No GPU detected. Installing CPU-based PyTorch...")
            subprocess.run([
                str(VENV_PATH / "bin/python3"), "-m", "pip", "install",
                "torch", "torchvision", "torchaudio"
            ], check=True)

        # Install remaining libraries
        print("Installing libraries from requirements.txt...")
        subprocess.run([
            str(VENV_PATH / "bin/python3"), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)
        ], check=True)

        print("Python dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Dependency installation failed: {e}")
        exit(1)  # Exit if dependencies fail to install


        print("Python dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Dependency installation failed: {e}")
        return download_and_install_tts()  # Fallback to direct TTS installation

def create_virtualenv():
    """
    Creates a virtual environment if it does not already exist.
    Sets 777 permissions for easy development cleanup.
    """
    if not VENV_PATH.exists():
        print("Creating virtual environment...")
        subprocess.run(["python3", "-m", "venv", str(VENV_PATH)], check=True)
        VENV_PATH.chmod(0o777)
        for root, dirs, files in os.walk(VENV_PATH):
            for dir_ in dirs:
                Path(os.path.join(root, dir_)).chmod(0o777)
            for file_ in files:
                Path(os.path.join(root, file_)).chmod(0o777)
        print("Virtual environment created successfully with 777 permissions.")
    else:
        print("Virtual environment already exists.")
    return "Virtual environment ready."



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

