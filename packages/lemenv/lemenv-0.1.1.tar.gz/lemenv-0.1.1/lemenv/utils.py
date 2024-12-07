from typing import List, Optional
import inquirer
from inquirer.themes import Theme
from colorama import init, Fore, Style
import os
import sys
from .manager import (
    create_venv, activate_venv, list_venvs, delete_venv, 
    recreate_venv, install_requirements, venv_info, get_venv_list
)
import subprocess
import time
import msvcrt  # For Windows key capture
import platform
import glob
from concurrent.futures import ThreadPoolExecutor

# Initialize colorama for cross-platform color support
init()

class LemEnvTheme(Theme):
    """Custom theme for LemEnv menus"""
    def __init__(self):
        super().__init__()
        self.Question.mark_color = Fore.GREEN
        self.Question.brackets_color = Fore.CYAN
        self.Question.default_color = Fore.WHITE
        self.List.selection_color = Fore.GREEN
        self.List.selection_cursor = "→"
        self.List.unselected_color = Fore.WHITE

def print_banner():
    """Display a beautiful ASCII banner"""
    banner = f"""
    {Fore.GREEN}╔═══════════════════════════════════════════════════╗
    ║                {Fore.YELLOW}🍋{Fore.CYAN} LemEnv{Fore.GREEN}                          ║
    ║   {Fore.YELLOW}A Citrus-Flavored Virtual Environment Manager{Fore.GREEN}   ║
    ║              {Fore.CYAN}from GenAI Jake!{Fore.GREEN}                     ║
    ╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def create_and_activate_venv(name: str):
    """Cross-platform virtual environment creation and activation"""
    try:
        if os.name == 'nt':  # Windows
            # Windows code remains the same
            activate_script = f"{name}_activate.ps1"
            with open(activate_script, 'w') as f:
                f.write(f"python -m venv {name}\n")
                f.write(f"Start-Process powershell -ArgumentList '-NoExit', '-Command', '.\\{name}\\Scripts\\Activate.ps1'\n")
            
            subprocess.Popen(['powershell', '-NoExit', '-File', activate_script], shell=True)
            time.sleep(1)
            os.remove(activate_script)
        else:  # Unix-like systems (Mac/Linux)
            create_cmd = f"python -m venv {name} && source {name}/bin/activate"
            
            # Check if we're on macOS
            if sys.platform == 'darwin':
                subprocess.run([
                    'osascript',
                    '-e',
                    f'tell application "Terminal" to do script "{create_cmd}"'
                ])
            else:
                # Try different Linux terminals
                terminal_cmds = [
                    ["gnome-terminal", "--", "bash", "-c", f"{create_cmd}; exec bash"],
                    ["konsole", "-e", f"bash -c '{create_cmd}; exec bash'"],
                    ["xterm", "-e", f"bash -c '{create_cmd}; exec bash'"],
                    ["x-terminal-emulator", "-e", f"bash -c '{create_cmd}; exec bash'"]
                ]
                
                for cmd in terminal_cmds:
                    try:
                        subprocess.Popen(cmd)
                        break
                    except FileNotFoundError:
                        continue
                    
    except Exception as e:
        print(f"{Fore.RED}Error creating/activating environment: {str(e)}{Style.RESET_ALL}")

def menu():
    banner = f"""
    {Fore.GREEN}╔═══════════════════════════════════════════════════╗
    ║                {Fore.YELLOW}🍋{Fore.CYAN} LemEnv{Fore.GREEN}                          ║
    ║   {Fore.YELLOW}A Citrus-Flavored Virtual Environment Manager{Fore.GREEN}   ║
    ║              {Fore.CYAN}from GenAI Jake!{Fore.GREEN}                     ║
    ╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
    """

    while True:
        print(banner)
        
        questions = [
            inquirer.List('action',
                message="What would you like to do?",
                choices=[
                    "Create a new virtual environment",
                    "Activate an existing virtual environment",
                    "List available virtual environments",
                    "Delete a virtual environment",
                    "Recreate a virtual environment",
                    "Install dependencies from requirements.txt",
                    "Show environment info",
                    "Exit"
                ],
            ),
        ]

        try:
            answers = inquirer.prompt(questions)
            if not answers:  # Handle escape key
                continue
                
            action = answers['action']

            if action == "Exit":
                print(f"\n{Fore.GREEN}Thanks for using LemEnv! Goodbye!{Style.RESET_ALL}")
                sys.exit(0)

            elif action == "Create a new virtual environment":
                # First, check if conda is available
                conda_available = False
                try:
                    subprocess.run(["conda", "--version"], 
                                 capture_output=True, check=True)
                    conda_available = True
                except Exception:
                    pass

                # Ask for environment type first
                type_question = [
                    inquirer.List('type',
                        message="Select environment type",
                        choices=["venv", "conda"] if conda_available else ["venv"],
                    ),
                ]
                
                type_answer = inquirer.prompt(type_question)
                if not type_answer:
                    continue

                # Set appropriate default name based on type
                default_name = "venv" if type_answer['type'] == "venv" else "conda_env"
                
                # Then ask for the name
                name_question = [
                    inquirer.Text('name',
                        message="Enter the name of the virtual environment",
                        default=default_name
                    ),
                ]
                
                name_answer = inquirer.prompt(name_question)
                if not name_answer:
                    continue

                create_venv(
                    name_answer['name'], 
                    type_answer['type']
                )
                continue

            elif action == "Activate an existing virtual environment":
                venvs = get_venv_list()
                if not venvs:
                    print(f"{Fore.RED}No virtual environments found!{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    continue
                
                questions = [
                    inquirer.List('name',
                        message="Select virtual environment to activate",
                        choices=venvs
                    )
                ]
                answers = inquirer.prompt(questions)
                if answers:
                    activate_venv(answers['name'])
                continue

            elif action == "List available virtual environments":
                list_venvs()
                input("\nPress Enter to continue...")
                continue

            elif action == "Delete a virtual environment":
                venvs = get_venv_list()
                
                if not venvs:
                    print(f"\n{Fore.YELLOW}No virtual environments found in current directory.{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    continue
                
                # Format choices with visual indicators
                choices = []
                for env_type, name in venvs:
                    type_indicator = "🔷" if env_type == "venv" else "🔶"
                    display_name = f"{type_indicator} {name} ({env_type})"
                    choices.append(display_name)
                
                questions = [
                    inquirer.List('env',
                        message="Select virtual environment to delete",
                        choices=choices
                    ),
                    inquirer.Confirm('confirm',
                        message=f"{Fore.YELLOW}⚠️  This action cannot be undone. Are you sure?{Style.RESET_ALL}",
                        default=False
                    )
                ]
                
                answers = inquirer.prompt(questions)
                if answers and answers['confirm']:
                    selected = answers['env']
                    name = selected.split(' ')[1]
                    env_type = selected.split('(')[1].rstrip(')')
                    
                    try:
                        delete_venv(name, env_type)
                    except Exception as e:
                        print(f"\n{Fore.RED}Failed to delete {name}: {str(e)}{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.YELLOW}Deletion cancelled.{Style.RESET_ALL}")
                
                input("\nPress Enter to continue...")
                continue

            elif action == "Recreate a virtual environment":
                venvs = get_venv_list()
                if not venvs:
                    print(f"{Fore.RED}No virtual environments found!{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    continue
                
                questions = [
                    inquirer.List('name',
                        message="Select virtual environment to recreate",
                        choices=venvs
                    ),
                    inquirer.Confirm('confirm',
                        message="Are you sure you want to recreate this virtual environment?",
                        default=False
                    )
                ]
                
                answers = inquirer.prompt(questions)
                if answers and answers['confirm']:
                    recreate_venv(answers['name'])
                input("\nPress Enter to continue...")
                continue

            elif action == "Install dependencies from requirements.txt":
                venvs = get_venv_list()
                if not venvs:
                    print(f"{Fore.RED}No virtual environments found!{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    continue
                
                questions = [
                    inquirer.List('name',
                        message="Select virtual environment",
                        choices=venvs
                    ),
                    inquirer.Text('requirements',
                        message="Enter the path to requirements.txt",
                        default="requirements.txt"
                    )
                ]
                
                answers = inquirer.prompt(questions)
                if answers:
                    install_requirements(answers['name'], answers['requirements'])
                input("\nPress Enter to continue...")
                continue

            elif action == "Show environment info":
                venvs = get_venv_list()
                if not venvs:
                    print(f"{Fore.RED}No virtual environments found!{Style.RESET_ALL}")
                    input("\nPress Enter to continue...")
                    continue

                # Format choices with visual indicators
                choices = []
                for env_type, name in venvs:
                    type_indicator = "🔷" if env_type == "venv" else "🔶"
                    display_name = f"{type_indicator} {name} ({env_type})"
                    choices.append(display_name)

                questions = [
                    inquirer.List('env',
                        message="Select virtual environment",
                        choices=choices
                    )
                ]

                answers = inquirer.prompt(questions)
                if answers:
                    selected = answers['env']
                    name = selected.split(' ')[1]
                    env_type = selected.split('(')[1].rstrip(')')
                    venv_info(name, env_type)

                input("\nPress Enter to continue...")
                continue

        except KeyboardInterrupt:
            if inquirer.prompt([inquirer.Confirm('confirm', 
                message="Do you want to exit?")
            ])['confirm']:
                print(f"\n{Fore.GREEN}Thanks for using LemEnv! Goodbye!{Style.RESET_ALL}")
                sys.exit(0)
            continue

if __name__ == "__main__":
    print("Starting LemEnv...")  # Debugging output
    menu()