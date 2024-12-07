import os
import subprocess
import shutil
import sys
from typing import Optional
from colorama import Fore, Style
import time
from concurrent.futures import ThreadPoolExecutor
import inquirer
import glob
import platform

def get_scripts_dir(venv_name: str) -> str:
    """Get the scripts directory path based on OS"""
    if sys.platform == "win32":
        return os.path.join(venv_name, "Scripts")
    return os.path.join(venv_name, "bin")

def get_python_path(venv_name: str) -> str:
    """Get the python executable path based on OS"""
    scripts_dir = get_scripts_dir(venv_name)
    if sys.platform == "win32":
        return os.path.join(scripts_dir, "python.exe")
    return os.path.join(scripts_dir, "python")

def show_spinner(duration: float, message: str):
    """Display a spinner animation while waiting"""
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for char in spinner:
            sys.stdout.write(f'\r{char} {message}')
            sys.stdout.flush()
            time.sleep(0.1)

def get_available_python_versions():
    """Get list of available Python versions on the system"""
    versions = []
    try:
        # Always add current Python version
        current_version = f"Current ({platform.python_version()})"
        versions.append(current_version)
        
        # Check for Python versions in common locations
        if os.name == 'nt':  # Windows
            python_paths = []
            # Check Python in Program Files
            program_files = [
                os.environ.get('ProgramFiles', 'C:\\Program Files'),
                os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
            ]
            for pf in program_files:
                python_paths.extend(glob.glob(os.path.join(pf, 'Python*')))
            
            # Check Python in AppData
            appdata = os.path.expanduser('~\\AppData\\Local\\Programs\\Python\\Python*')
            python_paths.extend(glob.glob(appdata))
            
            # Get versions from valid paths
            for path in python_paths:
                try:
                    if os.path.isdir(path):
                        python_exe = os.path.join(path, 'python.exe')
                        if os.path.exists(python_exe):
                            result = subprocess.run(
                                [python_exe, '--version'],
                                capture_output=True,
                                text=True
                            )
                            if result.returncode == 0:
                                version = result.stdout.strip()
                                if version not in versions:
                                    versions.append(version)
                except Exception:
                    continue
        
        else:  # Unix-like systems
            try:
                # Try to get versions from pyenv if installed
                result = subprocess.run(
                    ['pyenv', 'versions', '--bare'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    pyenv_versions = result.stdout.splitlines()
                    versions.extend([f"Python {v.strip()}" for v in pyenv_versions])
            except FileNotFoundError:
                pass
            
            # Try to find system Python versions
            for major in range(3, 12):  # Python 3.x through 11.x
                for minor in range(12):
                    try:
                        cmd = f"python{major}.{minor}"
                        result = subprocess.run(
                            [cmd, '--version'],
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            version = result.stdout.strip()
                            if version not in versions:
                                versions.append(version)
                    except FileNotFoundError:
                        continue
    
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Error getting Python versions: {str(e)}{Style.RESET_ALL}")
    
    # Remove duplicates and sort
    versions = list(dict.fromkeys(versions))
    
    # Make sure current version is first
    if current_version in versions:
        versions.remove(current_version)
        versions.insert(0, current_version)
    
    return versions

def create_venv(name: str, env_type: str = "venv"):
    """Create a new virtual environment"""
    try:
        if env_type == "venv":
            print(f"{Fore.CYAN}Creating venv environment: {name}{Style.RESET_ALL}")
            subprocess.run([sys.executable, "-m", "venv", name], check=True)
            
            print(f"{Fore.GREEN}✓ Successfully created venv environment: {name}{Style.RESET_ALL}")
            
            # Show activation command
            if os.name == 'nt':  # Windows
                cmd_activate = f"{name}\\Scripts\\activate.bat"
                ps_activate = f".\\{name}\\Scripts\\Activate.ps1"
                print(f"\n{Fore.GREEN}To activate in CMD:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{cmd_activate}{Style.RESET_ALL}")
                print(f"\n{Fore.GREEN}To activate in PowerShell:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{ps_activate}{Style.RESET_ALL}")
            else:  # Unix-like
                activate_cmd = f"source {name}/bin/activate"
                print(f"\n{Fore.GREEN}To activate, run:{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{activate_cmd}{Style.RESET_ALL}")
        
        else:  # conda
            print(f"{Fore.CYAN}Creating conda environment: {name}{Style.RESET_ALL}")
            
            # Create conda environment in current directory
            cmd = ["conda", "create", "--prefix", os.path.join(os.getcwd(), name), "python", "-y"]
            subprocess.run(cmd, check=True)
            
            print(f"{Fore.GREEN}✓ Successfully created conda environment: {name}{Style.RESET_ALL}")
            print(f"\n{Fore.GREEN}To activate, run:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}conda activate ./{name}{Style.RESET_ALL}")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}Failed to create environment: {str(e)}{Style.RESET_ALL}")
        return False

def activate_venv(name):
    """Show instructions to activate a virtual environment."""
    if not os.path.exists(name):
        print(f"{Fore.RED}Virtual environment '{name}' not found.{Style.RESET_ALL}")
        return

    if os.name == 'nt':  # Windows
        # Show both CMD and PowerShell commands
        cmd_activate = f"{name}\\Scripts\\activate.bat"
        ps_activate = f".\\{name}\\Scripts\\Activate.ps1"
        print(f"\n{Fore.GREEN}To activate in CMD:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{cmd_activate}{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}To activate in PowerShell:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{ps_activate}{Style.RESET_ALL}")
    else:  # Unix-like
        activate_cmd = f"source {name}/bin/activate"
        print(f"\n{Fore.GREEN}To activate, run:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{activate_cmd}{Style.RESET_ALL}")

def get_venv_list():
    """Get a list of all virtual environments in the current directory."""
    venvs = []
    current_dir = os.path.abspath('.')
    
    for item in os.listdir('.'):
        item_path = os.path.join(current_dir, item)
        if os.path.isdir(item_path):
            # Check for venv
            pyvenv_cfg = os.path.join(item_path, 'pyvenv.cfg')
            if os.path.exists(pyvenv_cfg):
                scripts_dir = get_scripts_dir(item_path)
                activate_path = os.path.join(scripts_dir, 'activate')
                if os.path.exists(activate_path):
                    venvs.append(('venv', item))
            # Check for conda
            elif os.path.exists(os.path.join(item_path, 'conda-meta')):
                venvs.append(('conda', item))
    
    return venvs

def list_venvs():
    """List all virtual environments."""
    venvs = get_venv_list()
    if venvs:
        print(f"\n{Fore.GREEN}Available virtual environments:{Style.RESET_ALL}")
        for env_type, name in venvs:
            type_indicator = "🔷" if env_type == "venv" else "🔶"
            print(f"  {type_indicator} {Fore.CYAN}{name}{Style.RESET_ALL} ({env_type})")
    else:
        print(f"{Fore.YELLOW}No virtual environments found.{Style.RESET_ALL}")

def delete_venv(name: str, env_type: str = "venv"):
    """Delete a virtual environment."""
    try:
        print(f"\n{Fore.YELLOW}Preparing to delete {env_type} environment: {name}{Style.RESET_ALL}")
        
        if env_type == "venv":
            if os.path.exists(name):
                print(f"{Fore.CYAN}Removing venv directory...{Style.RESET_ALL}")
                shutil.rmtree(name)
                print(f"{Fore.GREEN}✓ Virtual environment '{name}' has been deleted.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Virtual environment '{name}' not found.{Style.RESET_ALL}")
        else:  # conda
            env_path = os.path.join(os.getcwd(), name)
            if os.path.exists(env_path):
                print(f"{Fore.CYAN}Removing conda environment...{Style.RESET_ALL}")
                shutil.rmtree(env_path)
                print(f"{Fore.GREEN}✓ Conda environment '{name}' has been deleted.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Conda environment '{name}' not found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error deleting environment: {str(e)}{Style.RESET_ALL}")
        raise

def recreate_venv(name: str):
    """Recreate a virtual environment while preserving packages"""
    if not os.path.exists(name):
        print(f"{Fore.RED}Virtual environment '{name}' not found.{Style.RESET_ALL}")
        return False
        
    # Save installed packages
    pip_path = get_pip_path(name)
    requirements_backup = f"{name}_backup_requirements.txt"
    
    try:
        # Use pip freeze with proper redirection for both Windows and Unix
        with open(requirements_backup, 'w') as f:
            result = subprocess.run([pip_path, "freeze"], 
                                  capture_output=True, 
                                  text=True)
            if result.returncode == 0:
                f.write(result.stdout)
        
        if delete_venv(name) and create_venv(name):
            if os.path.exists(requirements_backup):
                install_requirements(name, requirements_backup)
                os.remove(requirements_backup)
                return True
    except Exception as e:
        print(f"{Fore.RED}Failed to recreate virtual environment: {str(e)}{Style.RESET_ALL}")
        if os.path.exists(requirements_backup):
            os.remove(requirements_backup)
        return False

def install_requirements(name: str, requirements: str):
    """Install requirements with progress indication"""
    pip_path = os.path.join(get_scripts_dir(name), "pip")
    
    if not os.path.exists(pip_path):
        print(f"{Fore.RED}Virtual environment '{name}' not found.{Style.RESET_ALL}")
        return False
        
    if not os.path.exists(requirements):
        print(f"{Fore.RED}Requirements file '{requirements}' not found.{Style.RESET_ALL}")
        return False
        
    print(f"{Fore.CYAN}Installing requirements from: {requirements}{Style.RESET_ALL}")
    
    try:
        subprocess.run([pip_path, "install", "-r", requirements], check=True)
        print(f"{Fore.GREEN}✓ Successfully installed requirements{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Failed to install requirements: {str(e)}{Style.RESET_ALL}")
        return False

def venv_info(name: str, env_type: str = "venv"):
    """Show information about a virtual environment."""
    try:
        if env_type == "venv":
            if not os.path.exists(name):
                print(f"{Fore.RED}'{name}' is not a valid virtual environment.{Style.RESET_ALL}")
                return

            # Get Python version from venv
            cfg_file = os.path.join(name, 'pyvenv.cfg')
            python_version = "Unknown"
            if os.path.exists(cfg_file):
                with open(cfg_file) as f:
                    for line in f:
                        if line.startswith('version'):
                            python_version = line.split('=')[1].strip()
                            break

            # Get installed packages
            pip_path = os.path.join(name, 'Scripts', 'pip.exe') if os.name == 'nt' else os.path.join(name, 'bin', 'pip')
            packages = []
            if os.path.exists(pip_path):
                result = subprocess.run([pip_path, 'freeze'], capture_output=True, text=True)
                if result.returncode == 0:
                    packages = result.stdout.splitlines()

            # Display information
            print(f"\n{Fore.GREEN}Environment Information:{Style.RESET_ALL}")
            print(f"  {Fore.CYAN}Name:{Style.RESET_ALL} {name}")
            print(f"  {Fore.CYAN}Type:{Style.RESET_ALL} venv")
            print(f"  {Fore.CYAN}Python Version:{Style.RESET_ALL} {python_version}")
            print(f"  {Fore.CYAN}Location:{Style.RESET_ALL} {os.path.abspath(name)}")
            print(f"\n{Fore.GREEN}Installed Packages:{Style.RESET_ALL}")
            if packages:
                for pkg in sorted(packages):
                    print(f"  - {pkg}")
            else:
                print("  No packages installed")

        else:  # conda
            env_path = os.path.join(os.getcwd(), name)
            if not os.path.exists(env_path):
                print(f"{Fore.RED}'{name}' is not a valid conda environment.{Style.RESET_ALL}")
                return

            # Get conda environment info
            try:
                # Get Python version
                python_path = os.path.join(env_path, 'python.exe') if os.name == 'nt' else os.path.join(env_path, 'bin', 'python')
                python_version = "Unknown"
                if os.path.exists(python_path):
                    result = subprocess.run([python_path, '--version'], capture_output=True, text=True)
                    if result.returncode == 0:
                        python_version = result.stdout.strip()

                # Get installed packages using conda list
                result = subprocess.run(['conda', 'list', '--prefix', env_path], capture_output=True, text=True)
                packages = []
                if result.returncode == 0:
                    # Skip the header lines
                    packages = [line for line in result.stdout.splitlines() if not line.startswith('#')]

                # Display information
                print(f"\n{Fore.GREEN}Environment Information:{Style.RESET_ALL}")
                print(f"  {Fore.CYAN}Name:{Style.RESET_ALL} {name}")
                print(f"  {Fore.CYAN}Type:{Style.RESET_ALL} conda")
                print(f"  {Fore.CYAN}Python Version:{Style.RESET_ALL} {python_version}")
                print(f"  {Fore.CYAN}Location:{Style.RESET_ALL} {env_path}")
                print(f"\n{Fore.GREEN}Installed Packages:{Style.RESET_ALL}")
                if packages:
                    for pkg in sorted(packages):
                        print(f"  - {pkg}")
                else:
                    print("  No packages installed")

            except Exception as e:
                print(f"{Fore.RED}Error getting conda environment info: {str(e)}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error getting environment info: {str(e)}{Style.RESET_ALL}")