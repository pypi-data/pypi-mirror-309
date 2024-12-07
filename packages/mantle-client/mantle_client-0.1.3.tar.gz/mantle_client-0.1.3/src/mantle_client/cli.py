from pathlib import Path
from subprocess import run
from loguru import logger
from typer import Typer, Context, Option, Exit

app = Typer(
    name="Mantle Client",
    pretty_exceptions_enable=False,
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

@app.command()
def notebook(
    ctx: Context,
    notebook_dir: Path = Option(
        Path.cwd().parent,
        "--notebook-dir",
        "-n",
        help="Directory to launch Jupyter Notebook (default: parent directory of the current working directory)",
    ),
):
    """Launch Jupyter Notebook in the specified directory."""
    try:
        notebook_dir = notebook_dir.resolve()
        logger.info(f"Launching Jupyter Notebook in directory: {notebook_dir}")
        run(["jupyter", "lab"], cwd=notebook_dir)
    except Exception as e:
        logger.error(f"Failed to launch Jupyter Notebook: {e}")
        raise Exit(1)

@app.command()
def logging():
    """Test logging."""
    logger.debug("Debug logging")
    logger.info("Info logging")
    

def main():
    app()


if __name__ == "__main__":
    main()
