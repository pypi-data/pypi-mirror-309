import time, os
from poisson_d.commands import measureit, create_img, create_points, rgb2cmyk
from poisson_d.poisson_d import Point
import imageio.v2 as iio
import numpy as np
from pathlib import Path
import pytest


def test_measureit():
    def dummy_function():
        time.sleep(0.1)
        return "test result"

    result = measureit(dummy_function)

    assert result == "test result"


def test_create_img(tmp_path: Path):
    height, width = 10, 10
    output = tmp_path / "test_image.png"

    points = [Point(x=1.5, y=1.5), Point(x=2.5, y=2.5), Point(x=3.5, y=3.5)]

    create_img(height, width, points, output)

    generated_image = iio.imread(output)

    assert generated_image.shape == (height, width, 3)

    assert np.array_equal(generated_image[1, 1], [0xFF, 0xFF, 0xFF])


def test_create_points(setup_points):
    points, output_path = setup_points

    create_points(points, output_path)

    assert os.path.exists(f"{output_path}_points.txt")
    assert os.path.exists(f"{output_path}_grey.txt")

    with open(f"{output_path}_points.txt", "r") as file_p:
        lines = file_p.readlines()
        assert lines[0].strip() == "{1,2,0}"
        assert lines[1].strip() == "{3,4,0}"

    with open(f"{output_path}_grey.txt", "r") as file_g:
        lines = file_g.readlines()
        assert lines[0].strip() == "0.5"
        assert lines[1].strip() == "0.8"


def test_rgb2cmyk():
    rgb = (255, 0, 0)
    expected_cmyk_normalized = [0, 1, 1, 0]
    assert rgb2cmyk(rgb, normalize=True) == expected_cmyk_normalized

    expected_cmyk_non_normalized = [0, 1, 1, 0]
    assert rgb2cmyk(rgb, normalize=False) == expected_cmyk_non_normalized

    rgb_black = (0, 0, 0)
    expected_cmyk_black = [0, 0, 0, 1]
    assert rgb2cmyk(rgb_black, normalize=True) == expected_cmyk_black

    rgb_white = (255, 255, 255)
    expected_cmyk_white = [0, 0, 0, 0]
    assert rgb2cmyk(rgb_white, normalize=True) == expected_cmyk_white
