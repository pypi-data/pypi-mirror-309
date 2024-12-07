from pathlib import Path
from datetime import datetime
import yaml
import typer
from rich import print
import os
from typing import Annotated


CONFIG_FILE = Path.home() / ".config" / "tool-create-project" / "config.yaml"

def load_config() -> dict:
    if not CONFIG_FILE.exists():
        # Create default config
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        default_config = {
            "project_location": "~/projects/personal/YYYY-MM"
        }
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(default_config, f)
        return default_config
    
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)

def get_project_path(base_path: str) -> Path:
    now = datetime.now()
    expanded_path = os.path.expanduser(base_path)
    return Path(expanded_path.replace('YYYY', str(now.year))
                           .replace('MM', f'{now.month:02d}'))

def create_project(
    project_name: Annotated[str, typer.Argument(help="Name of the project to create")]
):
    """
    Create a new project in the configured location
    """
    config = load_config()
    base_path = config.get('project_location')
    
    project_dir = get_project_path(base_path) / project_name
    
    if project_dir.exists():
        print(f"[red]Error:[/red] Project directory already exists: {project_dir}")
        raise typer.Exit(1)
    
    # Create project directory and basic structure
    project_dir.mkdir(parents=True)
    
    # Create basic project files
    (project_dir / "README.md").write_text(f"# {project_name}\n")
    
    print(f"[green]✓[/green] Created new project at: {project_dir}")