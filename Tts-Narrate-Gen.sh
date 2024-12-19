#!/bin/bash
# Script: `./Tts-Narrate-Gen.sh`

ENV_ACTIVE=0

print_header_separator() {
    echo "================================================================================"
}

print_footer_separator() {
    echo "--------------------------------------------------------------------------------"
}

check_python_version() {
    # Try different possible Python commands
    if command -v python3.12 >/dev/null 2>&1; then
        PYTHON_CMD="python3.12"
    elif command -v python3 >/dev/null 2>&1; then
        # Check if python3 is version 3.12
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if [[ "$PYTHON_VERSION" == "3.12" ]]; then
            PYTHON_CMD="python3"
        else
            echo "Error: Python 3.12 is required. Found version: $PYTHON_VERSION"
            sleep 3
            return 1
        fi
    elif command -v python >/dev/null 2>&1; then
        # Check if python is version 3.12
        PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if [[ "$PYTHON_VERSION" == "3.12" ]]; then
            PYTHON_CMD="python"
        else
            echo "Error: Python 3.12 is required. Found version: $PYTHON_VERSION"
            sleep 3
            return 1
        fi
    else
        echo "Error: Python 3.12 is not found!"
        sleep 3
        return 1
    fi

    echo "Python 3.12 found as command: $PYTHON_CMD"
    export PYTHON_CMD
    sleep 1
    return 0
}

check_sudo() {
    if [[ $EUID -ne 0 ]]; then
        echo "Error: Sudo Authorization Required!"
        exit 1
    fi
    echo "Sudo authorization confirmed."
}

activate_env_if_needed() {
    # Use the Python command we found earlier
    SYSTEM_PYTHON=$(which $PYTHON_CMD)
    
    if [ ! -d "./venv" ]; then
        echo "Virtual environment not found. Creating one now..."
        $PYTHON_CMD -m venv ./venv
        if [ $? -ne 0 ]; then
            echo "Error: Failed to create virtual environment. Check Python installation."
            exit 1
        fi
        chmod -R 777 ./venv
        echo "Virtual environment created successfully."
    fi
    source ./venv/bin/activate
    ENV_ACTIVE=1
    echo "Virtual environment activated."
}

deactivate_env_if_active() {
    if [ $ENV_ACTIVE -eq 1 ]; then
        deactivate
        ENV_ACTIVE=0
        echo "Virtual environment deactivated."
    fi
}

create_folders() {
    for folder in "./models" "./output" "./data"; do
        mkdir -p "$folder"
        chmod -R 777 "$folder"
    done
    echo "Directories created and permissions set."
}

install_requirements() {
    echo "Installing requirements..."
    # Use system Python to run pip in the virtual environment
    "./venv/bin/pip" install --upgrade pip
    "./venv/bin/pip" install gradio transformers torch pydub ffmpeg-python huggingface_hub PyYAML py3-tts
    echo "Requirements installed successfully."
}

manage_program_files() {
    print_header_separator
    echo "    Manage Program Files - Install or Remove"
    print_header_separator
    echo ""
    if [ -d "./data" ]; then
        echo "Program files are currently installed."
        echo "Would you like to remove them? (y/n)"
        read -r remove_choice
        if [[ "$remove_choice" =~ ^[Yy]$ ]]; then
            rm -rf ./venv ./data ./models ./output
            echo "Program files removed successfully."
        else
            echo "No changes made. Returning to menu..."
        fi
    else
        echo "Program files are not currently installed."
        echo "Would you like to install them? (y/n)"
        read -r install_choice
        if [[ "$install_choice" =~ ^[Yy]$ ]]; then
            if check_python_version; then
                create_folders
                activate_env_if_needed
                install_requirements
                echo "Program files installed successfully."
            else
                echo "Installation cancelled due to Python version requirement."
                return 1
            fi
        else
            echo "No changes made. Returning to menu..."
        fi
    fi
    deactivate_env_if_active
}

launch_program() {
    # Ensure the script runs from the correct directory
    SCRIPT_DIR=$(dirname "$(realpath "$0")")
    cd "$SCRIPT_DIR" || { echo "Error: Could not change to script directory."; exit 1; }

    # Check Python version before proceeding
    if ! check_python_version; then
        return 1
    fi

    # Store system Python path
    SYSTEM_PYTHON=$(which python)
    
    # Activate the virtual environment
    activate_env_if_needed

    echo "Running main_script.py using system Python..."
    "$SYSTEM_PYTHON" main_script.py

    # Deactivate the virtual environment after the script exits
    deactivate_env_if_active
}

End_Of_Script() {
    clear
    print_header_separator
    echo "    Tts-Narrate-Gen - Exit Sequence"
    print_header_separator
    echo ""
    echo "Menu Exited By User."
    deactivate_env_if_active
    echo "Exiting In 3 Seconds..."
    sleep 3
    exit 0
}

while true; do
    print_header_separator
    echo "    Tts-Narrate-Gen - Bash Menu"
    print_header_separator
    echo ""
    echo "    1. Launch Tts-Narrate-Gen"
    echo ""
    echo "    2. Check/Manage Libraries/Files"
    echo ""
    print_footer_separator
    echo -n "Selection; Menu Options = 1,2, Exit Program = X: "
    read -r choice
    case "$choice" in
        1) launch_program ;;
        2) manage_program_files ;;
        X|x) End_Of_Script ;;
        *) echo "Invalid option, try again." ;;
    esac
    sleep 2
done
