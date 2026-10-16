"""
ModelArena CLI
Usage:
  modelarena eval "Explain recursion" --models claude-haiku-5-5,gpt-4o-mini
  modelarena models
"""
import typer
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

app     = typer.Typer(help="ModelArena — evaluate AI models from your terminal")
console = Console()

API_BASE = "http://localhost:8000"


@app.command()
def eval(
    prompt: str = typer.Argument(..., help="Prompt to evaluate"),
    models: str  = typer.Option("claude-haiku-5-5,gpt-4o-mini", help="Comma-separated model IDs"),
    criteria: str = typer.Option("Accuracy,Clarity,Depth", help="Comma-separated criteria"),
    anthropic_key: str = typer.Option("", envvar="ANTHROPIC_API_KEY"),
    openai_key:    str = typer.Option("", envvar="OPENAI_API_KEY"),
    groq_key:      str = typer.Option("", envvar="GROQ_API_KEY"),
):
    """Evaluate a prompt across multiple models and display ranked results."""
    model_list    = [m.strip() for m in models.split(",")]
    criteria_list = [c.strip() for c in criteria.split(",")]

    console.print(f"\n[bold cyan]⬡ ModelArena[/] — evaluating across {len(model_list)} models…\n")

    with httpx.Client(timeout=60) as client:
        resp = client.post(f"{API_BASE}/evaluate/", json={
            "prompt": prompt,
            "models": model_list,
            "criteria": criteria_list,
            "api_keys": {
                "anthropic": anthropic_key,
                "openai":    openai_key,
                "groq":      groq_key,
            }
        })
        resp.raise_for_status()
        data = resp.json()

    evals    = sorted(data["evaluations"], key=lambda x: x["overall"], reverse=True)
    latencies = data.get("latencies", {})

    # ── Results table ──
    table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold dim")
    table.add_column("Rank", width=5)
    table.add_column("Model", style="bold")
    table.add_column("Overall", justify="center", width=9)
    for c in criteria_list:
        table.add_column(c, justify="center", width=9)
    table.add_column("Latency", justify="right", width=9)

    medals = ["🥇", "🥈", "🥉"]
    for i, ev in enumerate(evals):
        rank = medals[i] if i < 3 else f"#{i+1}"
        overall_color = "green" if ev["overall"] >= 8 else "yellow" if ev["overall"] >= 6 else "red"
        row = [
            rank,
            ev["model_id"],
            f"[{overall_color}]{ev['overall']}[/]",
        ]
        for c in criteria_list:
            s = ev.get("scores", {}).get(c, "—")
            color = "green" if isinstance(s, (int, float)) and s >= 8 else "yellow" if isinstance(s, (int, float)) and s >= 6 else "red"
            row.append(f"[{color}]{s}[/]")
        row.append(f"{latencies.get(ev['model_id'], '—')}ms")
        table.add_row(*row)

    console.print(table)
    console.print(Panel(
        f"[bold]Winner:[/] {data.get('winner', '—')}\n\n{data.get('comparison', '')}",
        title="💡 Insight", border_style="cyan"
    ))


@app.command()
def models():
    """List all available models."""
    with httpx.Client() as client:
        resp = client.get(f"{API_BASE}/models/")
        resp.raise_for_status()
        data = resp.json()

    table = Table(box=box.SIMPLE, header_style="bold dim")
    table.add_column("Model ID")
    table.add_column("Provider")
    table.add_column("API Key Needed")

    for m in data["models"]:
        table.add_row(m["id"], m["provider"], m["key_required"])

    console.print(table)


if __name__ == "__main__":
    app()
