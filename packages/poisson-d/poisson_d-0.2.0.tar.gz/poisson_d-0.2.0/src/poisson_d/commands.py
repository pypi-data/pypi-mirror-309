import math
from poisson_d import poisson_d as p

from rich.console import Console
from typing import List
import numpy as np, imageio.v3 as iio
import time
from pathlib import Path

console = Console()


def generate_image(
    image: Path,
    radius_min_max: tuple[int, int],
    max_points: int,
    output: Path,
    white_threshold: float,
):
    im = load_img(image)
    points = compute_points(im, radius_min_max, max_points, white_threshold)
    height, width, _ = im.shape
    create_img(height, width, points, output)


def generate_points(
    image: Path,
    radius_min_max: tuple[int, int],
    max_points: int,
    output: Path,
    white_threshold: float,
):
    im = load_img(image)
    points = compute_points(im, radius_min_max, max_points, white_threshold)
    create_points(points, output)


def compute_points(
    image: np.ndarray,
    radius_min_max: tuple[int, int],
    max_points: int,
    white_threshold: float,
) -> List[p.Point]:
    def execute() -> List[p.Point]:
        points = p.poisson_d_variant(
            img=image,
            radius_min_max=radius_min_max,
            max_points=max_points,
        )
        console.print(f"generated {len(points)} points")
        clean_points = p.filter_out_white(image, points, white_threshold)
        console.print(f"kept {len(clean_points)} points after white filtering")
        return clean_points

    return measureit(execute)


def generate_disc(
    height: int,
    width: int,
    radius: float,
    max_points: int,
    output: Path,
):
    def execute() -> List[p.Point]:
        points = p.poisson_d(
            height=height, width=width, min_dist=radius, max_points=max_points
        )
        console.print(f"generated {len(points)} points")
        return points

    points = measureit(execute)
    create_img(height, width, points, output)


def measureit(execution):
    start = time.time()
    result = execution()
    duration = time.time() - start
    console.print(f"duration: {math.ceil(duration * 100)/100} sec")
    return result


def generate_cmyk(
    image: Path,
    radius_min_max: tuple[int, int],
    max_points: int,
    output: Path,
    th: float,
):
    im = load_img(image)

    def execute() -> tuple[List[p.Point], List[p.Point], List[p.Point], List[p.Point]]:
        ((c, m, y, k), _) = p.poisson_d_cmyk(
            img=im, r=radius_min_max, n=max_points, th=th
        )
        console.print(f"generated {len(c) + len(m) + len(y) + len(k)} points")
        cc = p.filter_out_white(im, c, th)
        mm = p.filter_out_white(im, m, th)
        yy = p.filter_out_white(im, y, th)
        kk = p.filter_out_white(im, k, th)
        console.print(
            f"kept {len(cc) + len(mm) + len(yy) + len(kk)} points after white filtering"
        )
        return cc, mm, yy, kk

    c, m, y, k = measureit(execute)
    height, width, _ = im.shape
    create_img(height, width, c, f"{output}_c.png")
    create_img(height, width, m, f"{output}_m.png")
    create_img(height, width, y, f"{output}_y.png")
    create_img(height, width, k, f"{output}_k.png")


def create_img(height: int, width: int, points: List[p.Point], output: Path):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    for point in points:
        col, row = math.floor(point.x), math.floor(point.y)
        image[row, col, :] = (0xFF, 0xFF, 0xFF)

    iio.imwrite(output, image)
    console.print(f"image generated to {output}")


def create_points(points: List[p.Point], output: Path):
    with open(f"{output}_points.txt", "w") as file_p:
        with open(f"{output}_grey.txt", "w") as file_g:
            for point in points:
                file_p.write(f"{point.to_gh_point3d()}\n")
                file_g.write(f"{point.grey}\n")
    console.print(f"points generated to {output}")


def load_img(image: Path) -> np.ndarray:
    im = iio.imread(image)
    console.print(f"image {image}{im.shape} loaded")
    return im
