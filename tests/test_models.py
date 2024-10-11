"""Tests for statistics functions within the Model layer."""

import numpy as np
import numpy.testing as npt
import pytest
import math


def test_daily_mean_zeros():
    """Test that mean function works for an array of zeros."""
    from inflammation.models import daily_mean

    test_input = np.array([[0, 0],
                           [0, 0],
                           [0, 0]])
    test_result = np.array([0, 0])

    # Need to use Numpy testing functions to compare arrays
    npt.assert_array_equal(daily_mean(test_input), test_result)


def test_daily_mean_integers():
    """Test that mean function works for an array of positive integers."""
    from inflammation.models import daily_mean

    test_input = np.array([[1, 2],
                           [3, 4],
                           [5, 6]])
    test_result = np.array([3, 4])

    # Need to use Numpy testing functions to compare arrays
    npt.assert_array_equal(daily_mean(test_input), test_result)


def test_compute_stddev_by_day_one_row():
    from inflammation.models import compute_stddev_by_day

    data = np.array([[1], [3], [5]])

    result = compute_stddev_by_day(data)
    npt.assert_array_almost_equal(result, np.array([1.632993]))


def test_compute_stddev_by_day_multiple_rows():
    from inflammation.models import compute_stddev_by_day

    data = np.array([[1, 3, 5], [3, 3, 3], [10, 2, 2]])

    result = compute_stddev_by_day(data)
    npt.assert_array_almost_equal(result, np.array([0.785674]))


def test_compute_stddev_by_day_multiple_files():
    from inflammation.models import compute_stddev_by_day

    data = np.array([[1, 3, 5], [3, 3, 3], [10, 2, 2]])

    result = compute_stddev_by_day(data)
    npt.assert_array_almost_equal(result, np.array([0.785674]))

@pytest.mark.parametrize('data,expected_output', [
    ([[[0, 1, 0], [0, 2, 0]]], [0, 0, 0]),
    ([[[0, 2, 0]], [[0, 1, 0]]], [0, math.sqrt(0.25), 0]),
    ([[[0, 1, 0], [0, 2, 0]], [[0, 1, 0], [0, 2, 0]]], [0, 0, 0])
],
ids=['Two patients in same file', 'Two patients in different files', 'Two identical patients in two different files'])
def test_compute_standard_deviation_by_day(data, expected_output):
    from inflammation.models import compute_stddev_by_day

    result = compute_stddev_by_day(data)
    npt.assert_array_almost_equal(result, expected_output)