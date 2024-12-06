import typer

from tool_create_project.main import create_project

app = typer.Typer()
app.command()(create_project)

if __name__ == "__main__":
    app()