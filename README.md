# Danchro Auto Magic Stone Scramble

This is an script to auto queue for matches in the game "Danchro"
in the "Magic Stone Scramble" mode.

## Video Example




https://github.com/xcodinas/danchro-mss-autoqueue/assets/20686011/64fc22c4-2fe4-4d05-aa5b-0db5d3bce538




## Features

- **Automatic Game Startup**: The script automatically starts the game if it's not already running.
- **Game State Monitoring**: Monitors various aspects of the game's state, such as whether the player is currently in a match, waiting in a matchmaking queue, or has completed a match.
- **Menu Navigation**: Navigates through the game's menus to perform actions such as joining matches and accepting rewards.
- **Image Recognition**: Utilizes image recognition to detect elements on the screen, such as buttons and icons.

## Requirements

- Python 3.x
- Python packages: `psutil`, `pyautogui`

## Setup

1. Clone or download the repository to your local machine.
2. Install the required Python packages using `pip`:

    ```bash
    pip install psutil pyautogui
    ```

3. Ensure the game "Danchro" is installed on your system and the game executable path is correctly set in the script (`game_path` variable).

## Usage

Run the script using Python:

```bash
python auto-mss.py
```

The script will automatically start monitoring the game and perform actions based on its state.
The game should be in the main monitor and in the foreground for the script to work correctly.

## Notes

- The script may need adjustments based on the specific game version and screen resolution.

## Create Executable

To create an executable file from the script, you can use a tool such as `pyinstaller`:

```bash
pip install pyinstaller
pyinstaller --console --onefile --add-data "img/*;img/" auto-mss.py
```
