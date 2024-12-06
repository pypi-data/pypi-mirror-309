Let’s build **LemEnv** step-by-step from scratch using your Cursor IDE! 🎉

Here’s a roadmap to get it up and running:

---

## **Step 1: Set Up Your Project**

1. **Create a Directory**:
   Open your terminal in Cursor and create the project folder:
   ```bash
   mkdir lemenv
   cd lemenv
   ```

2. **Set Up a Python Virtual Environment for Development**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # (or `.\venv\Scripts\activate` on Windows)
   ```

3. **Install Necessary Packages**:
   Use `pip` to install the required libraries:
   ```bash
   pip install inquirer click colorama
   ```

4. **Set Up the Folder Structure**:
   Create the basic project structure:
   ```bash
   mkdir lemenv
   touch lemenv/__init__.py lemenv/cli.py lemenv/manager.py lemenv/utils.py
   touch setup.py README.md
   ```

---

## **Step 2: Implement Core Features**

### **1. CLI Entry Point (`cli.py`)**

Use `click` to handle the CLI interface and menu integration.

```python
import click
from lemenv.manager import (
    create_venv, activate_venv, list_venvs, delete_venv, recreate_venv, install_requirements, venv_info, get_venv_list
)
from lemenv.utils import menu

@click.group()
def cli():
    """LemEnv: A simple virtual environment manager."""
    pass

@cli.command()
@click.argument('name', default='venv')
def create(name):
    """Create a new virtual environment."""
    create_venv(name)

@cli.command()
@click.argument('name', default='venv')
def activate(name):
    """Activate an existing virtual environment."""
    activate_venv(name)

@cli.command()
def list():
    """List all virtual environments in the current directory."""
    list_venvs()

@cli.command()
@click.argument('name')
def delete(name):
    """Delete a virtual environment."""
    delete_venv(name)

@cli.command()
@click.argument('name', default='venv')
def recreate(name):
    """Recreate a virtual environment."""
    recreate_venv(name)

@cli.command()
@click.argument('name', default='venv')
@click.argument('requirements', default='requirements.txt')
def install(name, requirements):
    """Install dependencies from requirements.txt."""
    install_requirements(name, requirements)

@cli.command()
@click.argument('name', default='venv')
def info(name):
    """Show virtual environment info."""
    venv_info(name)

@cli.command()
def menu_command():
    """Launch the interactive menu."""
    menu()

if __name__ == "__main__":
    cli()
```

---

### **2. Add Interactive Menu (`utils.py`)**

Create a menu for users who want a guided experience.

```python
import inquirer
from lemenv.manager import (
    create_venv, activate_venv, list_venvs, delete_venv, recreate_venv, install_requirements, venv_info, get_venv_list
)

def menu():
    questions = [
        inquirer.List(
            "action",
            message="What would you like to do?",
            choices=[
                "Create a new virtual environment",
                "Activate an existing virtual environment",
                "List available virtual environments",
                "Delete a virtual environment",
                "Recreate a virtual environment",
                "Install dependencies from requirements.txt",
                "Show environment info",
                "Exit",
            ],
        )
    ]
    answers = inquirer.prompt(questions)
    action = answers["action"]

    if action == "Create a new virtual environment":
        name = input("Enter the name of the virtual environment (default: venv): ") or "venv"
        create_venv(name)
    elif action == "Activate an existing virtual environment":
        name = input("Enter the name of the virtual environment to activate: ")
        activate_venv(name)
    elif action == "List available virtual environments":
        list_venvs()
    elif action == "Delete a virtual environment":
        name = input("Enter the name of the virtual environment to delete: ")
        delete_venv(name)
    elif action == "Recreate a virtual environment":
        name = input("Enter the name of the virtual environment to recreate: ")
        recreate_venv(name)
    elif action == "Install dependencies from requirements.txt":
        name = input("Enter the name of the virtual environment: ")
        requirements = input("Enter the path to requirements.txt (default: ./requirements.txt): ") or "requirements.txt"
        install_requirements(name, requirements)
    elif action == "Show environment info":
        name = input("Enter the name of the virtual environment: ")
        venv_info(name)
    elif action == "Exit":
        print("Goodbye!")
        exit()
```

---

### **3. Core Virtual Environment Logic (`manager.py`)**

Add the functions for managing virtual environments.

```python
import os
import subprocess
import shutil

def create_venv(name):
    if os.path.exists(name):
        print(f"Virtual environment '{name}' already exists.")
    else:
        subprocess.run(["python", "-m", "venv", name])
        print(f"Created virtual environment: {name}")

def activate_venv(name):
    activate_script = os.path.join(name, "Scripts", "activate")
    if os.path.exists(activate_script):
        print(f"To activate, run: source {activate_script}")
    else:
        print(f"Virtual environment '{name}' not found.")

def list_venvs():
    venvs = [
        d for d in os.listdir(".")
        if os.path.isdir(d) and os.path.exists(os.path.join(d, "Scripts", "activate"))
    ]
    print("Available virtual environments:")
    for venv in venvs:
        print(f" - {venv}")

def delete_venv(name):
    if os.path.exists(name):
        shutil.rmtree(name)
        print(f"Deleted virtual environment: {name}")
    else:
        print(f"Virtual environment '{name}' not found.")

def recreate_venv(name):
    delete_venv(name)
    create_venv(name)

def install_requirements(name, requirements):
    pip_path = os.path.join(name, "Scripts", "pip")
    if os.path.exists(pip_path):
        subprocess.run([pip_path, "install", "-r", requirements])
    else:
        print(f"Virtual environment '{name}' not found.")

def venv_info(name):
    pip_path = os.path.join(name, "Scripts", "pip")
    if os.path.exists(pip_path):
        print(f"Virtual Environment Info for '{name}':")
        subprocess.run([pip_path, "freeze"])
    else:
        print(f"Virtual environment '{name}' not found.")

def get_venv_list():
    """Get a list of all virtual environments in the current directory."""
    venvs = []
    for item in os.listdir('.'):
        if os.path.isdir(item) and (
            os.path.exists(os.path.join(item, 'Scripts', 'activate')) or  # Windows
            os.path.exists(os.path.join(item, 'bin', 'activate'))  # Unix
        ):
            venvs.append(item)
    return venvs

def list_venvs():
    """List all virtual environments in the current directory."""
    venvs = get_venv_list()
    if venvs:
        print(f"\n{Fore.GREEN}Available virtual environments:{Style.RESET_ALL}")
        for venv in venvs:
            print(f"  - {Fore.CYAN}{venv}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}No virtual environments found.{Style.RESET_ALL}")
```

---

## **Step 3: Test the Application**
1. Run the application in Cursor’s terminal:
   ```bash
   python lemenv/cli.py menu
   ```

2. Test each command.

---

## **Step 4: Package for Distribution**
Add `setup.py` for packaging.

```python
from setuptools import setup, find_packages

setup(
    name="lemenv",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lemenv=lemenv.cli:cli'
        ]
    },
    install_requires=[
        'inquirer',
        'click',
        'colorama',
    ],
    description="A simple virtual environment manager.",
    author="Your Name",
    author_email="you@example.com",
)
```

Install the tool locally:
```bash
pip install -e .
```

You can now run:
```bash
lemenv menu
```

---

