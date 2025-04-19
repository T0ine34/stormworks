# Stormworks Projects

This repository contains various projects and scripts for enhancing the Stormworks game. Each folder represents a specific module or functionality.

## Project Structure

- **navlights/**: Contains scripts for controlling navigation lights.
  - `controller.lua`: Handles the logic for navigation light control.
  - `selector.lua`: Manages light selection.
  - `ship_draw.lua`: Draws ship-related visuals.

- **radar/**: Contains scripts for radar functionality.
  - `radar.lua`: Implements radar logic.

- **radioCommunication/**: Contains scripts for radio communication.
  - `keyboard.lua`: Handles keyboard input for radio communication.
  - `radio.lua`: Implements radio communication logic.

- **screenSwitcher/**: Contains scripts for switching between screens.
  - `script.lua`: Manages screen switching logic.

- **stormworks-externControl/**: A comprehensive project for external control of Stormworks.
  - Includes server components, front-end scripts, and configuration files.
  - Refer to the [README.md](stormworks-externControl/README.md) in this folder for detailed instructions.

## Getting Started

1. Clone the repository:
    ```sh
    git clone https://github.com/T0ine34/stormworks-projects.git
    cd stormworks-projects
    ```

2. Minify the scripts:
    ```sh
    make
    ```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.