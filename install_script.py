import os
import subprocess
from pathlib import Path
import yaml

PERSISTENT_FILE = Path("./data/persistent.yaml")
VENV_PATH = Path("./venv")
REQUIREMENTS_FILE = Path("./data/requirements.txt")
HARDWARE_FILE = Path("./data/hardware_details.txt")
FOLDERS_TO_CREATE = [
    "./models",   # Adjusted to create only this directory without subdirectories
    "./output",   # Directory for saving outputs
    "./data"
]

def check_sudo():
    """Check if the script is running as root."""
    if os.geteuid() != 0:
        print("Error: Sudo Authorization Required!")
        exit(1)
    print("Sudo authorization confirmed.")

def create_folders():
    for folder in FOLDERS_TO_CREATE:
        path = Path(folder)
        if not path.exists():
            print(f"Creating {folder} directory...")
            path.mkdir(parents=True, exist_ok=True)
            path.chmod(0o777)  # Ensure all created folders have 777 permissions
            print(f"{folder} directory created successfully.")
        else:
            print(f"{folder} directory already exists.")

def create_data_init_py():
    init_file = Path("./data/__init__.py")
    print("Creating or overwriting __init__.py in ./data")
    init_file.write_text("# This file marks this directory as a Python package.\n")
    init_file.chmod(0o777)
    print("__init__.py created successfully in ./data.")

def create_data_requirements():
    # Added TTS and other necessary libraries
    requirements = """gradio
transformers
torch
pydub
ffmpeg-python
huggingface_hub
PyYAML
TTS  # Ensure to specify the correct package name or PyPI name if different
"""
    print("Creating ./data/requirements.txt")
    REQUIREMENTS_FILE.write_text(requirements)
    REQUIREMENTS_FILE.chmod(0o777)
    print("./data/requirements.txt created successfully.")

def create_hardware_details():
    print("Detecting hardware information and creating hardware_details.txt in ./data")
    cpu_name = subprocess.getoutput("grep -m 1 'model name' /proc/cpuinfo | awk -F: '{print $2}'").strip()
    cpu_threads = subprocess.getoutput('lscpu | grep "^CPU(s):" | awk "{print $2}"').strip()
    system_ram = subprocess.getoutput('free -h | grep "Mem:" | awk "{print $2}"').strip()
    os_info = subprocess.getoutput('uname -a').strip()

    hardware_info = [
        f"CPU Name: {cpu_name}",
        f"CPU Threads Total: {cpu_threads}",
        f"Total System RAM: {system_ram}",
        f"OS Info: {os_info}"
    ]
    HARDWARE_FILE.write_text("\n".join(hardware_info))
    HARDWARE_FILE.chmod(0o777)
    print("Hardware details saved successfully to ./data/hardware_details.txt.")

def create_persistent_yaml():
    print("Creating or overwriting persistent.yaml in ./data")
    persistent_content = {
        "voice_model": "default",
        "speed": 1.0,
        "pitch": 1.0,
        "volume_gain": 0.0,
        "session_history": "",
        "threads_percent": 80,
        "model_path": "./models"  # Default model path
    }
    with open(PERSISTENT_FILE, 'w') as f:
        yaml.dump(persistent_content, f)
    PERSISTENT_FILE.chmod(0o777)
    print("persistent.yaml created successfully in ./data.")

def install_requirements():
    print(f"Installing from {REQUIREMENTS_FILE} to {VENV_PATH}")
    if REQUIREMENTS_FILE.exists():
        subprocess.run([str(VENV_PATH / "bin/python3"), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(VENV_PATH / "bin/python3"), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)], check=True)
        print("Python libraries installed successfully.")
    else:
        print(f"Error: {REQUIREMENTS_FILE} not found.")
        exit(1)

def create_virtualenv():
    """Create a virtual environment if it doesn't exist and set permissions."""
    venv_path = Path("./venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run(["python3", "-m", "venv", str(venv_path)], check=True)
        print("Virtual environment created.")
        venv_path.chmod(0o777)  # Set the directory permissions to 777
        print(f"Permissions set to 777 for {venv_path}")
    else:
        print("Virtual environment already exists.")

def main():
    print("Running the Setup-Installer for Gen-Gradio-Voice...")
    create_folders()
    create_persistent_yaml()
    create_data_init_py()
    create_data_requirements()
    create_virtualenv()
    install_requirements()
    create_hardware_details()
    print("Installer processes completed.")

if __name__ == "__main__":
    check_sudo()
    main()

