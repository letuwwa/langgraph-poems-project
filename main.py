import typer
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from poems.graph import build_graph
from poems.state import PoemState

app = typer.Typer()
console = Console()


def run_workflow(initial_state: PoemState) -> None:
    try:
        graph = build_graph()

        with console.status("Writing and checking..."):
            result = graph.invoke(initial_state)

    except Exception as exc:
        console.print("[red]Could not complete the poem workflow.[/red]")
        console.print(Text(str(exc)))
        raise typer.Exit(code=1) from exc

    title = "Your haiku" if initial_state["form"] == "haiku" else "The poem"

    console.print(
        Align.center(
            Panel.fit(
                Text(result["draft"], justify="left"),
                title=title,
                border_style="cyan",
            )
        )
    )

    if result["validation_errors"]:
        console.print("[yellow]Revision limit reached. These issues remain:[/yellow]")
        for error in result["validation_errors"]:
            console.print(Text(f"- {error}"))
    else:
        console.print("[green]Line-count check passed.[/green]")

    console.print(f"Revisions used: {result['revision_count']}")


@app.command()
def poem(
    topic: str,
    tone: str = "sad",
    lines: int = typer.Option(5, min=1, max=25),
) -> None:
    """Write a poem about TOPIC."""
    initial_state: PoemState = {
        "topic": topic,
        "tone": tone,
        "form": "poem",
        "target_lines": lines,
        "draft": "",
        "validation_errors": [],
        "revision_count": 0,
    }
    run_workflow(initial_state)


@app.command()
def haiku(
    topic: str,
    tone: str = "peaceful",
) -> None:
    """Write an English haiku about TOPIC."""
    initial_state: PoemState = {
        "topic": topic,
        "tone": tone,
        "form": "haiku",
        "target_lines": 3,
        "draft": "",
        "validation_errors": [],
        "revision_count": 0,
    }
    run_workflow(initial_state)


if __name__ == "__main__":
    app()
