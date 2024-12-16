# Tts-Narrate-Gen
Status: Alpha

### Description
The project is being set up with the intent to offer a Gradio-based interface for generating narrations. It utilizes advanced machine learning models to convert text into spoken audio, supporting multiple languages and voices. Tts-Narrate-Gen is designed to provide a user-friendly interface for generating narrations from text. The program can be used for various applications such as creating narrations for images, timed videos, or as part of multimedia presentations.

### FEATURES
- **Gradio Interface**: A web-based interface that allows users to interactively input text and generate narration.
  - **Narrator Page**: Features a single-column text box for user input and three buttons: "Gen Sample", "Play Narrate", and "Save As MP3".
  - **Configuration Page**: Allows users to configure TTS parameters, model settings, and view hardware details, with an "Update Settings" button for applying changes.
- **Dynamic Model Support**: Capable of loading and utilizing various TTS models, especially those available on Hugging Face, like [Hugging Face Voices](https://huggingface.co/voices).
- **Multi-Language and Multi-Speaker Support**: Supports generating speech in multiple languages and different speaker voices, making it versatile for various narration needs.
- **Automated File Management**: Manages audio output and settings configuration seamlessly through the interface.

### Preview
The application's interface is divided into two main parts:
- **Narration Interface Page**:

![Narration Interface](media/narration_interface.png)

- **Configuration Page**:

![Configuration Interface](media/configuration_interface.png)

- **Installer/Launcher**:
```
================================================================================
    Tts-Narrate-Gen - Bash Menu
================================================================================

    1. Launch Main Program

    2. Run Setup-Installer

--------------------------------------------------------------------------------
Selection; Menu Options = 1-2, Exit Program = X: 
```

### Requirements
- **Operating System**: Designed for Linux, Ubuntu/Debian compatible.
- **Dependencies**: Python 3, Gradio, PyTorch, and other necessary libraries installed within a virtual environment.

### Usage
1. **Installation**: Download the latest release and unpack it in a suitable directory.
2. **Setting Executable**: Ensure the launcher script is executable:
   ```bash
   chmod +x Tts-Narrate-Gen.sh
   ```
3. **Running the Program**:
   ```bash
   sudo ./Tts-Narrate-Gen.sh
   ```
   Follow the prompts to install dependencies or launch the main program.
4. **Web Interface**: Access the Gradio web interface at `http://127.0.0.1:7860` after launching the program.

### Development
Ongoing developments focus on enhancing model compatibility, improving interface usability, and expanding language support.

### Example Use Cases
Narrate educational content, provide audio for visual presentations, and facilitate language learning with diverse accents and dialects.

### File Structure
```
./
├── Tts-Narrate-Gen.sh        # Main Bash launcher script
├── main_script.py            # Main program script
├── install_script.py         # Installation script
├── data/
│   ├── persistent.yaml       # Stores user settings and configurations
├── models/                    # Directory to place model files
├── output/                   # Directory for generated audio files
└── README.md                 # Project documentation
```

## DISCLAIMER:
This project is currently in Alpha. Features and functionalities are subject to change as development progresses.
