#!/bin/bash
# Script: `./Anim-Narrate-Direct.sh`

ENV_ACTIVE=0

print_header_separator() {
    echo "================================================================================"
}

print_footer_separator() {
    echo "--------------------------------------------------------------------------------"
}

check_python_version() {
    # Check Python version
    if command -v python3.12 >/dev/null 2>&1; then
        PYTHON_CMD="python3.12"
    elif command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        [[ "$PYTHON_VERSION" == "3.12" ]] && PYTHON_CMD="python3" || { echo "Error: Python 3.12 required"; sleep 3; return 1; }
    elif command -v python >/dev/null 2>&1; then
        PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        [[ "$PYTHON_VERSION" == "3.12" ]] && PYTHON_CMD="python" || { echo "Error: Python 3.12 required"; sleep 3; return 1; }
    else
        echo "Error: Python 3.12 not found!"
        sleep 3
        return 1
    fi
    echo "Python found: $PYTHON_CMD"
    export PYTHON_CMD
    sleep 1
    return 0
}

check_sudo() {
    # Check sudo
    [[ $EUID -ne 0 ]] && { echo "Error: Sudo required!"; exit 1; }
    echo "Sudo confirmed."
}

activate_env_if_needed() {
    # Activate venv
    SYSTEM_PYTHON=$(which $PYTHON_CMD)
    [ ! -d "./venv" ] && { echo "Creating venv..."; $PYTHON_CMD -m venv ./venv || { echo "Error: Venv creation failed"; exit 1; }; chmod -R 777 ./venv; echo "Venv created."; }
    source ./venv/bin/activate
    ENV_ACTIVE=1
    echo "Venv activated."
}

deactivate_env_if_active() {
    # Deactivate venv
    [ $ENV_ACTIVE -eq 1 ] && { deactivate; ENV_ACTIVE=0; echo "Venv deactivated."; }
}

create_folders() {
    # Create folders
    for folder in "./models" "./output" "./data"; do
        mkdir -p "$folder"
        chmod -R 777 "$folder"
    done
    echo "Directories created."
}

install_requirements() {
    # Install requirements
    "./venv/bin/pip" install --upgrade pip
    "./venv/bin/pip" install speechbrain torchaudio pydub ffmpeg-python PyYAML torch gradio
    echo "Requirements installed."
}

create_persistent_yaml() {
    # Create persistent YAML
    PERSISTENT_FILE="./data/persistent.yaml"
    [ ! -f "$PERSISTENT_FILE" ] && {
        cat <<EOL > "$PERSISTENT_FILE"
model_path: "./models"
voice_model: "default"
speed: 1.0
pitch: 1.0
volume_gain: 0.0
threads_percent: 80
save_format: "mp3"
EOL
        echo "Persistent YAML created."
    } || echo "Persistent YAML exists."
}

manage_program_files() {
    # Manage program files
    print_header_separator
    echo "Manage Program Files"
    print_header_separator
    echo ""
    if [ -d "./data" ]; then
        echo "Files installed."
        echo "Remove? (y/n)"
        read -r remove_choice
        [[ "$remove_choice" =~ ^[Yy]$ ]] && { rm -rf ./venv ./data ./models ./output; echo "Files removed."; } || echo "No changes."
    else
        echo "Files not installed."
        echo "Install? (y/n)"
        read -r install_choice
        [[ "$install_choice" =~ ^[Yy]$ ]] && { check_python_version && { create_folders; activate_env_if_needed; install_requirements; create_persistent_yaml; echo "Files installed."; } || echo "Install cancelled."; } || echo "No changes."
    fi
    deactivate_env_if_active
}

launch_program() {
    # Check for models
    if [ -d "./models" ] && [ "$(ls -A ./models)" ]; then
        echo "Model Check: Pass"
        sleep 1
    else
        echo "Model Check: Fail"
        sleep 1
        echo "Insert model folders into ./models."
        sleep 3
        return 1
    fi

    # Launch program
    SCRIPT_DIR=$(dirname "$(realpath "$0")")
    cd "$SCRIPT_DIR" || { echo "Error: Script dir issue."; exit 1; }
    check_python_version || return 1
    SYSTEM_PYTHON=$(which python3.12)
    
    # Get the path to virtual environment's site-packages
    VENV_SITE_PACKAGES="$SCRIPT_DIR/venv/lib/python3.12/site-packages"
    
    # Add virtual environment's site-packages to PYTHONPATH
    export PYTHONPATH="$VENV_SITE_PACKAGES:$PYTHONPATH"
    
    echo "Running main_script.py with system Python and venv libraries"
    echo "PYTHONPATH set to: $PYTHONPATH"
    
    # Run with system Python but with access to venv libraries
    "$SYSTEM_PYTHON" main_script.py
}


End_Of_Script() {
    # Exit sequence
    clear
    print_header_separator
    echo "Exit Sequence"
    print_header_separator
    echo ""
    echo "Menu exited."
    deactivate_env_if_active
    echo "Exiting in 3s..."
    sleep 3
    exit 0
}

while true; do
    # Main menu
    print_header_separator
    echo "Anim-Narrate-Direct Menu"
    print_header_separator
    echo ""
    echo "1. Launch Tts-Narrate-Gen"
    echo ""
    echo "2. Manage Libraries/Files"
    echo ""
    print_footer_separator
    echo -n "Selection: 1,2, Exit=X: "
    read -r choice
    case "$choice" in
        1) launch_program ;;
        2) manage_program_files ;;
        X|x) End_Of_Script ;;
        *) echo "Invalid option." ;;
    esac
    sleep 2
done
