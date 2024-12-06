import click
from colorama import init, Fore, Style
from .manager import (
    create_venv, activate_venv, list_venvs, delete_venv, 
    recreate_venv, install_requirements, venv_info
)
from .utils import menu
import sys
import os

# Initialize colorama
init()

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """LemEnv: A citrus-flavored powerful virtual environment manager from GenAI Jake!
    
    Run without commands to start interactive mode.
    Use -h or --help to see available commands.
    """
    if ctx.invoked_subcommand is None:
        # If no subcommand was given, run the interactive menu
        menu()

@cli.command()
@click.argument('name', default='venv')
@click.option('--python', '-p', help='Python interpreter to use')
def create(name, python):
    """Create and activate a new virtual environment."""
    if os.name == 'nt':
        # PowerShell command
        create_cmd = f"python -m venv {name} && .\\{name}\\Scripts\\Activate.ps1"
        print(f"\n{Fore.GREEN}Copy and paste this command to create and activate:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{create_cmd}{Style.RESET_ALL}")
    else:
        # Unix command
        create_cmd = f"python -m venv {name} && source {name}/bin/activate"
        print(f"\n{Fore.GREEN}Copy and paste this command to create and activate:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{create_cmd}{Style.RESET_ALL}")
    sys.exit(0)

@cli.command()
@click.argument('name', default='venv')
def activate(name):
    """Show instructions to activate a virtual environment."""
    activate_venv(name)

@cli.command()
def list():
    """List all virtual environments."""
    list_venvs()

@cli.command()
@click.argument('name')
@click.option('--force', '-f', is_flag=True, help='Force deletion without confirmation')
def delete(name, force):
    """Delete a virtual environment."""
    if force or click.confirm(f"Are you sure you want to delete '{name}'?"):
        delete_venv(name)

@cli.command()
@click.argument('name', default='venv')
@click.option('--requirements', '-r', help='Save current requirements before recreating')
def recreate(name, requirements):
    """Recreate a virtual environment."""
    recreate_venv(name)

@cli.command()
@click.argument('name', default='venv')
@click.argument('requirements', default='requirements.txt')
def install(name, requirements):
    """Install dependencies from requirements file."""
    install_requirements(name, requirements)

@cli.command()
@click.argument('name', default='venv')
def info(name):
    """Show virtual environment information."""
    venv_info(name)

@cli.command()
def interactive():
    """Launch the interactive menu."""
    menu()

if __name__ == "__main__":
    cli() 