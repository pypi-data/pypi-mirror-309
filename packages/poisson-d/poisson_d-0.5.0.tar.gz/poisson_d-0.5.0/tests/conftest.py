import random
import pytest
import numpy as np
import imageio.v2 as iio
from poisson_d.poisson_d import Point


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


@pytest.fixture
def setup_points(tmp_path):
    # Prepare test data
    points = [Point(x=1, y=2, grey=0.5), Point(x=3, y=4, grey=0.8)]
    output_path = tmp_path / "test_output"
    return points, output_path
