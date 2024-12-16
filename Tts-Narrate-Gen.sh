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
    if [ $ENV_ACTIVE -eq 0 ]; then
        # Activate the virtual environment
        source ./venv/bin/activate
        ENV_ACTIVE=1
    fi
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
    python3 ./install_script.py
    if [ $? -ne 0 ]; then
        echo "Error: Installer encountered an issue."
    else
        echo "Installer completed successfully."
    fi
    sleep 2
    # Returns to menu with environment still active
}

# Function to launch the main program
launch_program() {
    print_header_separator
    echo "    Gen-Gradio-Voice - Launcher"
    print_header_separator
    echo ""
    echo "Preparing to launch the main program..."
    sleep 1

    activate_env_if_needed
    python3 ./main_script.py
    if [ $? -ne 0 ]; then
        echo "Error: Main program exited unexpectedly."
    else
        echo "Main program launched successfully."
    fi
    sleep 2
    # Returns to menu with environment still active
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

# Menu system
while true; do
    # clear
    print_header_separator
    echo "    Tts-Narrate-Gen - Bash Menu"
    print_header_separator
    echo ""
    echo "    1. Launch Main Program"
    echo ""
    echo "    2. Run Setup-Installer"
    echo ""
    print_footer_separator
    echo -n "Selection; Menu Options = 1-2, Exit Program = X: "
    read -r choice
    case "$choice" in
        1) launch_program ;;
        2) run_installer ;;
        X|x) End_Of_Script ;;
        *) echo "Invalid option, try again." ;;
    esac
    sleep 2
done

