"""Main module."""

from typing import List
from dataclasses import dataclass
import math
import random


@dataclass
class Point:
    y: float
    x: float
    grey: float = 0.0

    def in_rectangle(self, height: int, width: int) -> bool:
        """Check if a point is within the specified rectangle dimensions."""
        return 0 <= self.y <= height and 0 <= self.x <= width

    def to_gh_point3d(self) -> str:
        return f"{{{self.x},{self.y},0}}"


@dataclass
class Grid:
    height: int
    width: int
    rows: int
    cols: int
    cell_size: float
    points: List[List[List[Point]]]

    def add(self, point: Point, grey: float = 0.0):
        i, j = coord_to_cell(point, self.cell_size)
        if 0 <= i < self.rows and 0 <= j < self.cols:
            point.grey = grey
            self.points[i][j].append(point)
        else:
            raise IndexError(
                f"point out of Grid({self.cols}x{self.rows}): {(i, j)}-{point}"
            )


DEFAULT_MAX_POINTS = 20000
DEFAULT_CANDIDATES_COUNT = 25
DEFAULT_RADIUS_RANGE = (2, 15)
DEFAULT_WHITE_THRESHOLD = 0.9


def poisson_d(
    height: int,
    width: int,
    min_dist: float,
    candidates_count: int = DEFAULT_CANDIDATES_COUNT,
    max_points=DEFAULT_MAX_POINTS,
) -> List[Point]:
    image = zeros(height, width, 3)

    return poisson_d_variant(image, (min_dist, min_dist), candidates_count, max_points)


def zeros(rows: int, cols: int, dim: int) -> List[List[List[int]]]:
    return [[[0 for _ in range(dim)] for _ in range(cols)] for _ in range(rows)]


def compute_cell_size(radius: int) -> float:
    return radius / math.sqrt(2)


def create_grid(
    height: int,
    width: int,
    cell_diagnal: float,
) -> Grid:
    cell_size = compute_cell_size(cell_diagnal)
    rows, cols = math.ceil(height / cell_size), math.ceil(width / cell_size)
    points = [[[] for _ in range(cols)] for _ in range(rows)]
    return Grid(
        height=height,
        width=width,
        rows=rows,
        cols=cols,
        cell_size=cell_size,
        points=points,
    )


def random_point(height_limit: float, width_limit: float) -> Point:
    y = random.uniform(0, height_limit)
    x = random.uniform(0, width_limit)
    return Point(y, x, 0)


def coord_to_cell(point: Point, cell_size: float) -> tuple[int, int]:
    return (
        math.floor(point.y / cell_size),
        math.floor(point.x / cell_size),
    )


def generate_point_around(point: Point, min_dist: float) -> Point:
    r1 = random.randint(0, 100) / 100.0
    r2 = random.randint(0, 100) / 100.0

    radius = min_dist * (1 + r1)
    angle = 2 * math.pi * r2

    return Point(
        point.y + radius * math.sin(angle),
        point.x + radius * math.cos(angle),
    )


def is_neighbour(grid: Grid, point: Point, min_dist: float) -> bool:
    """
    check if the point is a neighber, akka too close
    """
    target_cell = coord_to_cell(point, grid.cell_size)
    related_cells = cells_around(grid, target_cell, 5)
    for cell in related_cells:
        i, j = cell
        for other in grid.points[i][j]:
            if distance(point, other) < min_dist:
                return True

    return False


def distance(one: Point, other: Point) -> float:
    """
    compute the distance between 2 points
    """
    return math.sqrt((one.x - other.x) ** 2 + (one.y - other.y) ** 2)


def cell_to_square(cell: tuple[int, int], cell_size: float) -> tuple[Point, Point]:
    """
    get the 4 extreme points (left_bottom, left_top, right_top, right_bottom) of the cell
    """
    row, column = cell
    left_bottom = Point(row * cell_size, column * cell_size)
    right_top = Point((1 + row) * cell_size, (1 + column) * cell_size)
    return left_bottom, right_top


def cells_around(
    grid: Grid, center_cell: tuple[int, int], size: int
) -> List[tuple[int, int]]:
    delta = math.floor(size / 2)
    row, colmn = center_cell
    result = []
    for i in range(row - delta, row + delta + 1):
        for j in range(colmn - delta, colmn + delta + 1):
            if grid.rows > i >= 0 and grid.cols > j >= 0:
                points = grid.points[i][j]
                cell: tuple[int, int] = (i, j)
                if len(points) > 0:
                    result.append(cell)
    return result


def rgb2gray(rgb: List[int]) -> float:
    return dot(rgb[:3], [0.2989, 0.5870, 0.1140]) / 0xFF


def single2grey(singleton: List[float]) -> float:
    return singleton[0]


def grey2rgb(grey: float) -> List[int]:
    return [
        grey / 3 / 0.2989 * 0xFF,
        grey / 3 / 0.5870 * 0xFF,
        grey / 3 / 0.1140 * 0xFF,
    ]


def dot(rgb: List[int], weights: List[float]) -> float:
    if len(rgb) != 3 or len(weights) != 3:
        raise ValueError("only lists of 3 elements are acceptable!")

    return rgb[0] * weights[0] + rgb[1] * weights[1] + rgb[2] * weights[2]


class RandomQueue:
    def __init__(self):
        self.items = []

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def not_empty(self) -> bool:
        return not self.is_empty()

    def size(self) -> int:
        return len(self.items)

    def push(self, item) -> None:
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("cannot pop from empty queue")
        index = random.randint(0, len(self.items) - 1)
        return self.items.pop(index)


def poisson_d_variant(
    img: List[List[List[int]]],
    radius_min_max: tuple[float, float] = DEFAULT_RADIUS_RANGE,
    candidates_count: int = DEFAULT_CANDIDATES_COUNT,
    max_points=DEFAULT_MAX_POINTS,
    grey_func=rgb2gray,
) -> List[Point]:
    """
    algorithm explained here: http://devmag.org.za/2009/05/03/poisson-disk-sampling/
    """
    height, width = len(img), len(img[0])
    _, max_radius = radius_min_max
    grid = create_grid(height, width, max_radius)
    to_process = RandomQueue()
    sample_points = []

    first_point = random_point(height, width)
    i, j = coord_to_cell(first_point, grid.cell_size)
    grid.add(first_point, grey_func(img[i][j]))
    to_process.push(first_point)
    sample_points.append(first_point)

    while to_process.not_empty() and len(sample_points) <= max_points:
        point = to_process.pop()
        min_dist = min_dist_from(radius_min_max, point, img, grey_func)
        for _ in range(candidates_count):
            new_point = generate_point_around(point, min_dist)
            if new_point.in_rectangle(height, width) and not is_neighbour(
                grid, new_point, min_dist
            ):
                to_process.push(new_point)
                sample_points.append(new_point)
                i, j = coord_to_cell(new_point, grid.cell_size)
                grid.add(new_point, grey_func(img[i][j]))

    return sample_points


def compute_min_dist(radius_min_max: tuple[float, float], greyscale: float) -> float:
    min_radius, max_radius = radius_min_max
    return min_radius + greyscale * (max_radius - min_radius)


def min_dist_from(
    radius_min_max: tuple[float, float],
    point: Point,
    img: List[List[List[int]]],
    grey_func,
) -> float:
    i, j = math.floor(point.y), math.floor(point.x)
    height, width = len(img), len(img[0])
    grey1 = grey_func(img[max(0, i - 1)][j])
    grey2 = grey_func(img[min(height - 1, i + 1)][j])
    grey3 = grey_func(img[i][max(0, j - 1)])
    grey4 = grey_func(img[i][min(width - 1, j + 1)])
    grey = (grey1 + grey2 + grey3 + grey4) / 4
    min_dist = compute_min_dist(radius_min_max, grey)
    return min_dist


def filter_out_white(
    img: List[List[List]],
    points: List[Point],
    threshold: float = 0.9,
    grey_func=rgb2gray,
) -> List[Point]:
    result = []
    for point in points:
        i, j = math.floor(point.y), math.floor(point.x)
        grey = grey_func(img[i][j])
        if grey <= threshold:
            result.append(point)

    return result


def normalize(color: int) -> float:
    return color / 0xFF


def rgb_to_cmyk(rgb: List[int]) -> List[float]:
    rgb = rgb[:3]
    r = normalize(rgb[0])
    g = normalize(rgb[1])
    b = normalize(rgb[2])
    # 确保 RGB 值的范围在 0-1 之间
    r = max(0, min(r, 1))
    g = max(0, min(g, 1))
    b = max(0, min(b, 1))

    # 计算 CMY 值
    c = 1 - r
    m = 1 - g
    y = 1 - b

    # 计算 K 值
    k = min(c, m, y)

    # 防止全黑时的特殊情况
    if k == 1:
        c = 0
        m = 0
        y = 0
    else:
        # 调整 C, M, Y
        c = (c - k) / (1 - k)
        m = (m - k) / (1 - k)
        y = (y - k) / (1 - k)

    return [c, m, y, k]


def extract_cmyk(
    img: List[List[List[int]]],
) -> tuple[List[float], List[float], List[float], List[float]]:
    rows, cols = len(img), len(img[0])
    cmyk = [[rgb_to_cmyk(img[i][j]) for j in range(cols)] for i in range(rows)]
    c = [[[cmyk[i][j][0]] for j in range(cols)] for i in range(rows)]
    m = [[[cmyk[i][j][1]] for j in range(cols)] for i in range(rows)]
    y = [[[cmyk[i][j][2]] for j in range(cols)] for i in range(rows)]
    k = [[[cmyk[i][j][3]] for j in range(cols)] for i in range(rows)]
    return c, m, y, k


def poisson_d_cmyk(
    img: List[List[List[int]]],
    r: tuple[float, float] = DEFAULT_RADIUS_RANGE,
    cnt: int = DEFAULT_CANDIDATES_COUNT,
    n=DEFAULT_MAX_POINTS,
    th=DEFAULT_WHITE_THRESHOLD,
) -> tuple[
    tuple[List[Point], List[Point], List[Point], List[Point]],
    tuple[List[Point], List[Point], List[Point], List[Point]],
]:
    c, m, y, k = extract_cmyk(img)
    c_poisson = poisson_d_variant(c, r, cnt, n, single2grey)
    print(f"generated {len(c_poisson)} points for c")
    c_poisson = filter_out_white(c, c_poisson, th, single2grey)
    m_poisson = poisson_d_variant(m, r, cnt, n, single2grey)
    print(f"generated {len(m_poisson)} points for m")
    m_poisson = filter_out_white(m, m_poisson, th, single2grey)
    y_poisson = poisson_d_variant(y, r, cnt, n, single2grey)
    print(f"generated {len(y_poisson)} points for y")
    y_poisson = filter_out_white(y, y_poisson, th, single2grey)
    k_poisson = poisson_d_variant(y, r, cnt, n, single2grey)
    print(f"generated {len(k_poisson)} points for k")
    k_poisson = filter_out_white(k, k_poisson, th, single2grey)

    return ((c_poisson, m_poisson, y_poisson, k_poisson), (c, m, y, k))


"""
import rhinoscriptsyntax as rs
import imageio.v3 as iio

image = iio.imread(img_path)

result = poisson_d_variant(
    img=image,
    radius_min_max=(radius_min, radius_max),
    max_points=max_points,
)

print(f"generated {len(result)} points")

result = filter_out_white(image, result, white_threshold)

coordinates = [rs.CreatePoint(pn.x, -pn.y, 0) for pn in result]
greys = [x.grey for x in result]

print("result size:", len(coordinates), len(greys))


import rhinoscriptsyntax as rs
import imageio.v3 as iio

image = iio.imread(img_path)

((c_points, m_points, y_points, k_points), (c, m, y, k)) = poisson_d_cmyk(
    img=image,
    r=(radius_min, radius_max),
    cnt=max_points,
    th=white_threshold,
)
"""
