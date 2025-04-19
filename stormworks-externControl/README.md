# Stormworks ExternControl

Stormworks ExternControl is a project designed to provide external control capabilities for the Stormworks game. This project includes a server component, front-end scripts, and various configuration files.

## Requirements

- Python 3.12 or higher
- Node.js
- npm (Node Package Manager)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/T0ine34/stormworks-externControl.git
    cd stormworks-externControl
    ```

> You only need to do steps below if you want to edit the project. If you only want to use the server, please refer to the [Usage](#usage) section.

2. **Set up the Python virtual environment:**

    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install Python dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Install Node.js dependencies:**

    ```sh
    npm install
    ```

## Compilation

To compile the project, run the following command:

```sh
make all
```

This will compile all the necessary files and place the output in the dist directory.

## Usage

To start the server, run the following command:

```sh
make start
```

This will compile the project, install the server, and start it.


## Running Tests

To run the tests, run the following command:

```sh
make tests
```

This will compile the project, install the server, and run the tests using pytest.

## License
This project is licensed under the MIT License.