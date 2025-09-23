![Mangetamain Logo](docs/images/logo.jpeg)

# Mangetamain

## Prerequisites

- Python>=3.12,<3.13
- Poetry
- Git

### Install Python 3.12

**For Windows**:

Download and install Python on your system: https://www.python.org/downloads/release/python-31210/

**For Mac**:

```commandline
brew install python@3.12
```
Test Python installed

```commandline
python3.12 --version
```

### Install Poetry (for packaging and dependency management)

Install the latest version of [Poetry](https://python-poetry.org/)

```commandline
pip3.12 install poetry
```

Test Poetry installed:
```commandline
poetry --version
```

Until now, we are always based on the native Python environment **NOT** the desired virtual environment.
Even Poetry is always run within this native Python environment.



### Install Git (for version control)

Install [Git](https://git-scm.com/downloads) and [set up it](https://docs.github.com/fr/get-started/git-basics/set-up-git)

## Installation

The following guidelines show how to install the project and set up a virtual environment isolated within the project folder.
### Clone the repo to your local

Clone the repository from GitHub (remote repo) to your local machine. This creates a copy of the code that you can modify locally. Your changes will take effect once you `commit` them and `push` to the remote repository (`add` files when necessary):

```commandline
cd /your/folder
git clone https://github.com/Hugosh71/Projet_Mangetamain.git
```

This clones the repo to `/your/folder/Projet_Mangetamain` with a hidden `.git` folder inside, which keeps track of everything about the code.

We don't need to redo `git init`, because the repo is already initialized (with a `.git`) when created from GitHub. Once cloned to your local machine, it's ready!

Now, you may open the repo from your code editor (VSCode).

### Set up the virtual environment

From now on, we recommend executing commands from the terminal in VS Code.  You can open a new terminal with `Terminal > New Terminal`. As a reminder, currently we are still using the native Python environment.

The pyproject.toml file contains all Poetry configurations. Inside, you can find the following lines:

```toml
requires-python = ">=3.12,<3.13"
dependencies = [
    "streamlit (>=1.49.1,<2.0.0)"
]
```

These lines specify the Python version and the dependencies used for the virtual environment.

**Create a virtual environment with specified dependencies:**

```commandline
poetry config virtualenvs.in-project true
poetry env use python3.12
poetry install
```

This creates `.venv` under your working folder. The `.venv` is an isolated environment containing own Python interpreter and its own set of dependencies (packages).

### Activate the virtual environment

**Option 1**

In VSCode, open the Command Palette (Ctrl + Shift + P or Command + Shift + P). Enter "Python" and click "Python: Select Interpreter". Then select the environment you've just created (for example, `mangetamain-py3.12`).

Reopen the terminal. If you see the (mangetamain-py3.12) prefix, the environment is **activated** from the VSCode terminal for this project.

**Option 2**

For Windows:

```commandline
.\.venv\Scripts\activate.ps1
```

For Mac:

```commandline
source .venv/bin/activate
```

If you see the (mangetamain-py3.12) prefix, the environment is **activated** from the VSCode terminal for this project.

Then you may use `pip freeze` to check whether `streamlit` is installed. If `streamlit` exist in the list of dependencies, the virtual environment is ready and we can start a local backend and web app servers later!

## Run locally

```commandline
make requirements
make run
```

The app will be available at `http://localhost:8501`.

## Collaborative Development

**Fetch changes from the remote repo on GitHub:**

```commandline
git fetch
```

or fetch & merge changes from the remote repo:

```commandline
git pull
```

**Commit and push changes to the remote repo:**

```commandline
# When necessary, add all modified files and prepare for next commit
git add .

# Save changes with a message
git commit -m "..."

# Push changes to the remote repo
git push
```

**Create a new branch:**

```commandline
# Create a new branch
git branch <branch-name>

# Switch to the new branch
git checkout <branch-name>
```

**Merge a branch to main:**

```commandline
git checkout main
git merge new-feature
```

If there are conflicts, Git will ask you to resolve them manually. After resolving:

```commandline
git add <file-with-conflict>
git commit -m "..."
```
