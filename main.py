import typer
from langchain_ollama import ChatOllama
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


app = typer.Typer()
console = Console()


@app.command()
def poem(
    topic: str,
    tone: str = "sad",
    lines: int = typer.Option(5, min=1, max=25),
):
    """Write a poem about TOPIC."""
    model = ChatOllama(
        model="gemma2:9b",
        temperature=0.8,
    )

    prompt = (
        f"Write a poem about: {topic}\n"
        f"Tone: {tone}\n"
        f"Length: exactly {lines} nonempty lines.\n"
        "Return only the poem, without a title or explanation."
    )

    try:
        with console.status("Writing your poem..."):
            response = model.invoke(prompt)
    except Exception as exc:
        console.print(
            "[red]Could not generate the poem.[/red] "
            "Check that Ollama is running and gemma2:9b is installed."
        )
        console.print(Text(str(exc)))
        raise typer.Exit(code=1) from exc

    console.print(
        Align.center(
            Panel.fit(
                Text(str(response.content).strip(), justify="left"),
                title="The poem",
                border_style="cyan",
            )
        )
    )


if __name__ == "__main__":
    app()
