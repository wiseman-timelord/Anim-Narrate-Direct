#!/bin/bash
# Script: `./Tts-Narrate-Gen.sh`

# Track if the virtual environment is active
ENV_ACTIVE=0

# Function to print a header separator
print_header_separator() {
    echo "================================================================================"
}

# Function to print a footer separator
print_footer_separator() {
    echo "--------------------------------------------------------------------------------"
}

# Function to check if running as root
check_sudo() {
    if [[ $EUID -ne 0 ]]; then
        echo "Error: Sudo Authorization Required!"
        sleep 3
        exit 1
    else
        echo "Sudo authorization confirmed."
        sleep 1
    fi
}

activate_env_if_needed() {
    if [ ! -d "./venv" ]; then
        echo "Virtual environment not found. Creating one now..."
        python3.11 -m venv ./venv
        if [ $? -ne 0 ]; then
            echo "Error: Failed to create virtual environment. Check Python installation."
            exit 1
        fi
        chmod -R 777 ./venv
        echo "Virtual environment created successfully."
    fi

    # Activate the virtual environment
    source ./venv/bin/activate
    ENV_ACTIVE=1
    echo "Virtual environment activated."
}

# Function to install Python 3.11.9 from source
install_python_3_11() {
    print_header_separator
    echo "    Install Python 3.11.9 - From Source"
    print_header_separator
    echo ""

    # Check if Python 3.11.9 is already installed
    if python3.11 --version 2>/dev/null | grep -q "Python 3.11.9"; then
        echo "Python 3.11.9 already installed."
        sleep 1
        echo "Returning to menu..."
        sleep 3
        return
    fi

    # If not installed, proceed with installation
    check_sudo
    echo "Installing required dependencies..."
    sudo apt update
    sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev \
    libssl-dev libreadline-dev libffi-dev wget libsqlite3-dev libbz2-dev

    echo "Downloading Python 3.11.9 source..."
    cd /usr/src
    sudo wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz
    sudo tar xzf Python-3.11.9.tgz

    echo "Building Python 3.11.9..."
    cd Python-3.11.9
    sudo ./configure --enable-optimizations
    sudo make altinstall

    echo "Verifying Python 3.11 installation..."
    python3.11 --version

    echo "Python 3.11.9 installed successfully."
    sleep 2
}


# Function to run the installer
run_installer() {
    print_header_separator
    echo "    Tts-Narrate-Gen - Installer"
    print_header_separator
    echo ""
    echo "Checking admin privileges..."
    check_sudo
    echo ""
    echo "Activating virtual environment and running installer..."
    sleep 1

    activate_env_if_needed
    python3.11 ./install_script.py
    if [ $? -ne 0 ]; then
        echo "Error: Installer encountered an issue."
    else
        echo "Installer completed successfully."
    fi
    sleep 2
}

# Function to delete installer-created files (except models and output)
delete_created_files() {
    print_header_separator
    echo "    Remove Installation - Cleanup"
    print_header_separator
    echo ""

    echo "Deleting files and folders created by the installer..."
    rm -rf ./venv ./data ./TTS-0.22.0 ./TTS.zip ./install_script.pyc ./__pycache__

    # Preserve 'models' and 'output'
    if [ -d "./models" ]; then
        echo "Preserving 'models' folder."
    fi
    if [ -d "./output" ]; then
        echo "Preserving 'output' folder."
    fi

    echo "Cleanup completed successfully."
}

# Function for the Install And Remove Submenu
install_and_remove_menu() {
    while true; do
        # clear #-- commented out for debugging options.
        print_header_separator
        echo "    Tts-Narrate-Gen - Install And Remove"
        print_header_separator
        echo ""
        echo "    1. Install Python 3.11.9"
        echo ""
        echo "    2. Run Program Installer"
        echo ""
        echo "    3. Remove Program Files"
        echo ""
        print_footer_separator
        echo -n "Selection; Menu Options = 1-3, Back To Main = B: "
        read -r choice
        case "$choice" in
            1) install_python_3_11 ;;
            2) run_installer ;;
            3) delete_created_files ;;
            B|b) break ;;
            *) echo "Invalid option, try again." ;;
        esac
        sleep 2
    done
}

# Function to activate venv and launch the program
launch_program() {
    # Absolute path to the virtual environment's Python interpreter
    VENV_PYTHON="./venv/bin/python3.11"

    # Check if Python 3.11.9 exists in venv
    if [ ! -f "$VENV_PYTHON" ]; then
        echo "Error: Python 3.11.9 not found in virtual environment. Please run the installer."
        exit 1
    fi

    # Activate the virtual environment
    echo "Activating virtual environment..."
    source ./venv/bin/activate

    # Confirm Python version in venv
    echo "Using Python version: $($VENV_PYTHON --version)"

    # Run the main Python script using the venv interpreter
    echo "Running main_script.py with virtual environment Python..."
    $VENV_PYTHON ./main_script.py

    # Deactivate the virtual environment after program exit
    deactivate
}



# Function to gracefully end the script
End_Of_Script() {
    clear
    print_header_separator
    echo "    Tts-Narrate-Gen - Exit Sequence"
    print_header_separator
    echo ""
    echo "Menu Exited By User."
    sleep 1
    if [ $ENV_ACTIVE -eq 1 ]; then
        echo "De-Activating VEnv."
        deactivate
    else
        echo "No active VEnv to deactivate."
    fi
    sleep 1
    echo "Exiting In 3 Seconds..."
    sleep 3
    exit 0
}

# Main menu system
while true; do
    # clear  #-- commented out for debugging options.
    print_header_separator
    echo "    Tts-Narrate-Gen - Bash Menu"
    print_header_separator
    echo ""
    echo "    1. Launch Main Program"
    echo ""
    echo "    2. Install And Remove"
    echo ""
    print_footer_separator
    echo -n "Selection; Menu Options = 1-2, Exit Program = X: "
    read -r choice
    case "$choice" in
        1) launch_program ;;
        2) install_and_remove_menu ;;
        X|x) End_Of_Script ;;
        *) echo "Invalid option, try again." ;;
    esac
    sleep 2
done

