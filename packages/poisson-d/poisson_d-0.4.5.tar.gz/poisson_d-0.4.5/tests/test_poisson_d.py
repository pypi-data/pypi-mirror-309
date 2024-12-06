#!/usr/bin/env python

"""Tests for `poisson_d` package."""

import math
from typing import List
import numpy as np
import pytest
import random
import timeit
import imageio.v3 as iio


from poisson_d import poisson_d as p


@pytest.fixture
def min_height() -> int:
    return 20


@pytest.fixture
def min_width() -> int:
    return 20


@pytest.fixture
def max_height() -> int:
    return 3072


@pytest.fixture
def max_width() -> int:
    return 4096


@pytest.fixture
def height(min_height, max_height) -> int:
    return random.randint(min_height, max_height)


@pytest.fixture
def width(min_width, max_width) -> int:
    return random.randint(min_width, max_width)


@pytest.fixture
def min_dist(min_height, min_width) -> float:
    min_min_dist = max(min_height, min_width)
    return random.randint(min_min_dist * 100, min_min_dist * 40 * 100) / 100.0


@pytest.fixture
def candidates_count() -> int:
    return 25


@pytest.fixture
def radius_min_max() -> tuple[int, int]:
    return 20, 200


@pytest.fixture
def img() -> np.ndarray:
    return iio.imread("input/sample.jpg")


def test_compute_cell_size(min_dist):
    cell_size = p.compute_cell_size(min_dist)
    assert cell_size == min_dist / math.sqrt(2)


def test_create_grid():
    grid = p.create_grid(15, 10, math.sqrt(2))
    assert grid.rows == 15
    assert grid.cols == 10
    assert len(grid.points) == 15
    assert len(grid.points[0]) == 10


def test_random_queue():
    """Test for RandomQueue functionality."""
    queue = p.RandomQueue()
    queue.push(1)
    queue.push(2)
    queue.push(3)

    assert queue.pop() in [1, 2, 3]
    assert queue.size() == 2
    assert queue.pop() in [1, 2, 3]
    assert queue.pop() in [1, 2, 3]
    assert queue.is_empty()


def test_random_point():
    """Test for random_point function."""
    width_limit = 10
    height_limit = 5
    point = p.random_point(height_limit, width_limit)

    assert 0 <= point.y <= height_limit
    assert 0 <= point.x <= width_limit
    assert isinstance(point, p.Point)


def test_coord_to_cell():
    """Test for coord_to_cell function."""
    cell_size = 2.0
    point = p.Point(4.5, 3.5, 0)
    cell = p.coord_to_cell(point, cell_size)

    assert cell == (2, 1)


def test_generate_point_around():
    """Test for generate_point_around function."""
    point = p.Point(5.0, 5.0, 0)
    min_dist = 2.0
    new_point = p.generate_point_around(point, min_dist)

    distance = math.sqrt((new_point.x - point.x) ** 2 + (new_point.y - point.y) ** 2)
    assert distance >= min_dist
    assert distance <= 2 * min_dist


def test_grid_in_rectangle():
    """Test for Grid's in_rectangle method."""

    point_inside = p.Point(3.0, 2.0)
    point_inside2 = p.Point(5.0, 5.0)
    point_outside = p.Point(3.0, 6.0)

    assert point_inside.in_rectangle(5, 5) is True
    assert point_inside2.in_rectangle(5, 5) is True
    assert point_outside.in_rectangle(5, 5) is False


def test_cell_to_square():
    """Test for cell_to_square function."""
    cell_size = 2.0
    cell = (1, 1)
    left_bottom, right_top = p.cell_to_square(cell, cell_size)

    expected_left_bottom = p.Point(1 * cell_size, 1 * cell_size)  # (2.0, 2.0)
    expected_right_top = p.Point((1 + 1) * cell_size, (1 + 1) * cell_size)  # (4.0, 4.0)

    assert left_bottom == expected_left_bottom
    assert right_top == expected_right_top


def test_distance_point_to_point():
    """Test for distance_point_to_cell function."""
    assert p.distance(p.Point(4, 3), p.Point(4, 3)) == pytest.approx(0, rel=1e-9)
    assert p.distance(p.Point(1, 3), p.Point(6, 3)) == pytest.approx(5, rel=1e-9)
    assert p.distance(p.Point(2, 3), p.Point(2, 1)) == pytest.approx(2, rel=1e-9)
    assert p.distance(p.Point(2, 2), p.Point(3, 3)) == pytest.approx(
        math.sqrt(2), rel=1e-9
    )


def test_cells_around():
    """Test for cells_around function."""
    rows, cols = 10, 10
    grid = p.create_grid(rows, cols, math.sqrt(2))
    for i in range(rows):
        for j in range(cols):
            grid.add(p.Point(i, j))

    assert len(p.cells_around(grid, (3, 4), 5)) == 25
    assert len(p.cells_around(grid, (1, 2), 5)) == 20
    assert len(p.cells_around(grid, (0, 0), 5)) == 9


def test_is_neighbour():
    """Test for is_neighbour function."""
    min_dist = 1.0
    grid = p.create_grid(10 * math.sqrt(2), 10 * math.sqrt(2), min_dist)
    grid.add(p.Point(y=2.221531969606713, x=1.9419891722697926))

    point_neighbour = p.Point(y=1.398757961353612, x=1.8441077365907659)
    point_not_neighbour = p.Point(7.0, 7.0)

    # Check if the points are neighbors
    assert p.is_neighbour(grid, point_neighbour, min_dist) is True
    assert p.is_neighbour(grid, point_not_neighbour, min_dist) is False


def test_poisson_d(height, width, min_dist, candidates_count):
    """Test for poisson_d_work function."""
    cell_size = p.compute_cell_size(min_dist)

    def execute() -> List[p.Point]:
        return p.poisson_d(width, height, min_dist, candidates_count)

    execution_time = timeit.timeit(execute, number=1)
    sample_points = execute()

    assert len(sample_points) > 0

    # Check if all points are within the specified width and height
    for point in sample_points:
        point.in_rectangle(height, width)

    # Check if the minimum distance between points is respected
    print(
        f"image({width}x{height})-distance({min_dist}) -> {len(sample_points)} points in {math.ceil(execution_time * 1000)/1000} sec"
    )
    for i in range(len(sample_points)):
        for j in range(i + 1, len(sample_points)):
            one, other = sample_points[i], sample_points[j]
            distance = math.sqrt((one.x - other.x) ** 2 + (one.y - other.y) ** 2)
            cellI = p.coord_to_cell(one, cell_size)
            cellJ = p.coord_to_cell(other, cell_size)
            assert (
                distance - min_dist > -0.001
            ), f"too close: {one} in cell({cellI}) vs {other} in cell({cellJ})"


def test_rgb2grey():
    assert p.rgb2gray((0xFF, 0xFF, 0xFF)) == pytest.approx(1, rel=0.001)
    assert p.rgb2gray((0, 0, 0)) == pytest.approx(0, rel=0.001)
    assert p.rgb2gray((150, 10, 99)) == pytest.approx(0.24310196078431373, rel=0.001)


def test_compute_min_dist():
    test_cases = [
        ((1.0, 5.0), 0.0, 1.0),
        ((1.0, 5.0), 0.5, 3.0),
        ((2.0, 6.0), 1.0, 6.0),
        ((0.0, 10.0), 0.0, 0.0),
    ]

    for radius_min_max, grey, expected in test_cases:
        result = p.compute_min_dist(radius_min_max, grey)
        assert result == pytest.approx(expected)


def test_poisson_d_variant(img, radius_min_max, candidates_count):
    """Test for poisson_d_work function."""

    def execute() -> List[p.Point]:
        return p.poisson_d_variant(img, radius_min_max, candidates_count)

    execution_time = timeit.timeit(execute, number=1)
    sample_points = execute()

    assert len(sample_points) > 0

    # Check if all points are within the specified width and height
    height, width, _ = img.shape
    for point in sample_points:
        point.in_rectangle(height, width)

    # Check if the minimum distance between points is respected
    print(
        f"image({width}x{height})-radius({radius_min_max}) -> {len(sample_points)} points in {math.ceil(execution_time * 1000)/1000} sec"
    )
    r_min, r_max = radius_min_max
    cell_size = p.compute_cell_size(r_max)
    for i in range(len(sample_points)):
        for j in range(i + 1, len(sample_points)):
            one, other = sample_points[i], sample_points[j]
            distance = math.sqrt((one.x - other.x) ** 2 + (one.y - other.y) ** 2)
            cellI = p.coord_to_cell(one, cell_size)
            cellJ = p.coord_to_cell(other, cell_size)
            assert (
                distance - r_min > -0.001
            ), f"too close: {one} in cell({cellI}) vs {other} in cell({cellJ})"


def test_add_method():
    grid = p.create_grid(2, 2, math.sqrt(2))

    point = p.Point(y=0.5, x=0.5)

    grid.add(point)

    assert len(grid.points[0][0]) == 1, "Point was not added to the grid."
    assert (
        grid.points[0][0][0] == point
    ), "The added point does not match the expected point."


def test_filter_out_white():
    img = np.array(
        [
            [[255, 255, 255], [255, 255, 255], [255, 255, 255]],  # White
            [[0, 0, 0], [128, 128, 128], [255, 255, 255]],  # Black, Grey, White
            [[255, 255, 255], [0, 0, 0], [255, 255, 255]],  # White, Black, White
        ],
        dtype=np.uint8,
    )

    points = [
        p.Point(0, 0),  # White
        p.Point(1, 1),  # Grey
        p.Point(2, 1),  # Black
    ]

    filtered_points = p.filter_out_white(img, points)

    assert len(filtered_points) == 2
    assert filtered_points[0].y == 1 and filtered_points[0].x == 1
    assert filtered_points[1].y == 2 and filtered_points[1].x == 1


# Tests for the dot function
def test_dot_valid_input():
    rgb = [255, 255, 255]
    weights = [0.2989, 0.5870, 0.1141]
    result = p.dot(rgb, weights)
    assert result == pytest.approx(255)


def test_dot_zero_input():
    rgb = [0, 0, 0]
    weights = [0.2989, 0.5870, 0.1140]
    result = p.dot(rgb, weights)
    assert result == 0.0


def test_dot_invalid_length():
    rgb = [255, 255]
    weights = [0.2989, 0.5870, 0.1140]
    with pytest.raises(ValueError):
        p.dot(rgb, weights)


# Tests for the zeros function
def test_zeros_valid_input():
    rows, cols, dim = 2, 3, 4
    result = p.zeros(rows, cols, dim)
    expected = [[[0 for _ in range(dim)] for _ in range(cols)] for _ in range(rows)]
    assert result == expected


def test_zeros_zero_dimensions():
    rows, cols, dim = 0, 0, 0
    result = p.zeros(rows, cols, dim)
    assert result == []


def test_zeros_non_zero_dim():
    rows, cols, dim = 2, 2, 0
    result = p.zeros(rows, cols, dim)
    expected = [[[] for _ in range(cols)] for _ in range(rows)]
    assert result == expected


def test_normalize():
    assert p.normalize(0) == 0.0
    assert p.normalize(255) == 1.0
    assert p.normalize(128) == 128 / 255
    assert p.normalize(0xFF) == 1.0
    assert p.normalize(0x00) == 0.0
    assert p.normalize(100) == 100 / 255


def test_rgb_to_cmyk():
    # Test cases: (RGB input, expected CMYK output)
    test_cases = [
        ([255, 0, 0], [0, 1, 1, 0]),  # Red
        ([0, 255, 0], [1, 0, 1, 0]),  # Green
        ([0, 0, 255], [1, 1, 0, 0]),  # Blue
        ([0, 0, 0], [0, 0, 0, 1]),  # Black
        ([255, 255, 255], [0, 0, 0, 0]),  # White
        ([128, 128, 128], [0, 0, 0, 0.5]),  # Gray
        ([255, 255, 0], [0, 0, 1, 0]),  # Yellow
        ([0, 255, 255], [1, 0, 0, 0]),  # Cyan
        ([255, 0, 255], [0, 1, 0, 0]),  # Magenta
    ]

    for rgb, expected_cmyk in test_cases:
        assert p.rgb_to_cmyk(rgb) == pytest.approx(expected_cmyk, rel=1e-2)


def test_extract_cmyk():
    test_image = [
        [[255, 0, 0], [0, 255, 0], [0, 0, 255]],  # Red, Green, Blue
        [[255, 255, 0], [0, 255, 255], [255, 0, 255]],  # Yellow, Cyan, Magenta
        [[0, 0, 0], [255, 255, 255], [128, 128, 128]],  # Black, White, Gray
    ]

    expected_cmyk = (
        [[0, 1, 1], [1, 0, 1], [1, 1, 0]],  # C
        [[0, 0, 1], [1, 0, 0], [0, 0, 0]],  # M
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],  # Y
        [[0, 0, 0], [0, 0, 0], [0.5, 0.5, 0.5]],  # K
    )

    c, m, y, k = p.extract_cmyk(test_image)

    assert len(c) == 3 and len(c[0]) == 3
    assert len(m) == 3 and len(m[0]) == 3
    assert len(y) == 3 and len(y[0]) == 3
    assert len(k) == 3 and len(k[0]) == 3
