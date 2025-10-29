# Prerequisites

Before installing Mangetamain, ensure you have the following prerequisites:

* Python >= 3.12, < 3.13
* Poetry (for dependency management)
* Git (for version control)

## Installing Python 3.12

For Windows

1. Download Python 3.12 from the official website: [https://www.python.org/downloads/release/python-31210/](https://www.python.org/downloads/release/python-31210/)
2. Run the installer and make sure to check “Add Python to PATH”
3. Verify the installation:

```cmd
python --version
```

For macOS

Using Homebrew:

```bash
brew install python@3.12
```

Verify the installation:

```bash
python3.12 --version
```

## For Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

## Installing Poetry

Poetry is used for dependency management and virtual environment handling.

```bash
pip3.12 install poetry
```

Verify the installation:

```bash
poetry --version
```

## Installing Git

Download and install Git from [https://git-scm.com/downloads](https://git-scm.com/downloads) and follow the setup instructions.
