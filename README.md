Tts-Narrate-Gen

    Status: Alpha
    Note: The README.md includes initial project setup details. Features and interfaces are near complete, but updates and enhancements are ongoing. See the development branch for the latest updates.

Description

Tts-Narrate-Gen is a Python-based text-to-speech application that utilizes advanced machine learning models to generate speech from text. It features a user-friendly Gradio interface, allowing users to input text and produce narrated audio seamlessly. This tool is designed to support various applications, including narration for images or timed videos, making it versatile for both personal and professional use.

FEATURES

    Multilingual and Multi-Speaker Model: Utilizes 🐸TTS models capable of voice cloning and language selection.
    Gradio Interface: Browser-based interactive interface for straightforward operation and immediate feedback.
    Integrated Setup and Operation: Includes a Bash script that handles setup, execution, and shutdown of the application.
    Configurable Model Path: Users can specify the model directory for flexible model management.
    File and Folder Management: Automates the handling of configuration files and outputs.
    Modularity: Designed with separate scripts for interface logic, model handling, and utility functions.
    Persistence: Retains session settings and configurations across restarts using YAML-based storage.

Preview

    The Narrator Page...

preview_image

    The Configuration Page...

preview_image

    The Installer/Launcher...

================================================================================
    Tts-Narrate-Gen - Bash Menu
================================================================================
    1. Launch Main Program
    2. Run Setup-Installer
--------------------------------------------------------------------------------
Selection; Menu Options = 1-2, Exit Program = X: 

Requirements

    Operating System: Linux, Ubuntu/Debian compatible.
    Python Environment: Local Python installation within `./venv` to avoid system conflicts.
    Python Libraries: Requires specific libraries like `gradio`, `torch`, and `TTS` which are installed via the setup script.
    Hardware: Supports CPU-based operations, with potential expansions for GPU usage in future updates.
    Internet Connection: Needed for downloading dependencies and model files.

Usage

To get started with Tts-Narrate-Gen:

    Download the latest release suitable for your system and extract it to a desired directory.
    Open a terminal in the extracted directory and run the following command to make the Bash script executable:
        chmod +x Tts-Narrate-Gen.sh
    Execute the script with:
        ./Tts-Narrate-Gen.sh
    Use the menu to run the Setup-Installer (Option 2) to install necessary libraries and set up the environment.
    Once setup is complete, launch the main program using Option 1. This will open the Gradio interface in your default web browser.
    Navigate to the Gradio interface to start interacting with the TTS system. Configure model paths and settings in the 'Configuration' tab.
    To exit, close the Gradio interface and select 'Exit Program' from the Bash menu to ensure proper shutdown.

Example Prompts

    "Hello there! What's the story today?"
    "Can you narrate the text from the following image for me?"
    "Adjust the pitch and speed to match a cheerful tone."

Notation

    Recommended models for testing: https://huggingface.co/voices for diverse language and voice options.
    Note on GPU Support: Currently optimized for CPU usage, with plans to support NVIDIA CUDA in future iterations.

File Structure

Initial File Structure...

./
├── Tts-Narrate-Gen.sh        # Main Bash launcher script
├── main_script.py            # Primary script for TTS operations
├── install_script.py         # Script for setting up the environment
├── data/ 
│   ├── persistent.yaml       # Stores configuration and session data
├── models/                   # Directory for storing model files
├── output/                   # Directory for generated audio files
└── requirements.txt          # Lists dependencies for the project

    Files Created by Installation...

./
├── venv/                     # Virtual environment directory
│   ├── *                     # Contains installed Python libraries.
├── logs/                     # Directory for log files (if implemented).
