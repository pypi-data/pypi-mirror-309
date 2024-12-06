"""Console script for poisson_d."""

from poisson_d import commands as cmd

import typer
from rich.console import Console
from enum import Enum
from pathlib import Path


app = typer.Typer()
console = Console()


class Action(Enum):
    Disk = "disk"
    Image = "image"
    Cmyk = "cmyk"
    Points = "points"


@app.command()
def main(
    action: Action = typer.Argument(Action.Disk.value),
    image: Path = typer.Option(Path("input/sample.jpg")),
    radius_min_max: tuple[int, int] = typer.Option((2, 15)),
    radius: float = typer.Option(30),
    height: int = typer.Option(600),
    width: int = typer.Option(800),
    max_points: int = typer.Option(30000),
    output: Path = typer.Option(Path("output/output.png")),
    white_threshold: float = typer.Option(0.8),
):
    console.print(f"running {action.value}")
    if action == Action.Image:
        cmd.generate_image(image, radius_min_max, max_points, output, white_threshold)
    elif action == Action.Cmyk:
        cmd.generate_cmyk(image, radius_min_max, max_points, output, white_threshold)
    elif action == Action.Disk:
        cmd.generate_disk(height, width, radius, max_points, output)
    elif action == Action.Points:
        cmd.generate_points(image, radius_min_max, max_points, output, white_threshold)


if __name__ == "__main__":
    app()
