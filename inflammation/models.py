"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains 
inflammation data for a single patient taken over a number of days 
and each column represents a single day across all patients.
"""

import numpy as np


def load_csv(filename):
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load
    :raises FileNotFoundError: raised if the filename cannot be found
    :returns: 2D np.ndarray
    """
    return np.loadtxt(fname=filename, delimiter=',')


def daily_mean(data):
    """Calculate the daily mean of a 2D inflammation data array.

    :param data: 2D-numpy array with patients on rows and days on columns
    :raises AxisError: raised if data is not an array
    :returns: np.ndarray
    """
    return np.mean(data, axis=0)


def daily_max(data):
    """Calculate the daily max of a 2D inflammation data array.

    :param data: 2D-numpy array with patients on rows and days on columns
    :raises AxisError: raised if data is not an array
    :returns: np.ndarray
    """
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily min of a 2D inflammation data array.

    :param data: 2D-numpy array with patients on rows and days on columns
    :raises AxisError: raised if data is not an array
    :returns: np.ndarray
    """
    return np.min(data, axis=0)


def patient_normalise(data):
    """Normalise patient data from a 2D inflammation data array.

    NaN values are ignored and normalised to 0.

    :param data: 2D numpy array with patients on rows and days on columns
    :raises ValueError: in case data contains values below 0
    :returns: np.ndarray, an array with the same shape as data, but values normalised
    """

    if np.any(data < 0):
        raise ValueError('Inflammation values should not be negative')

    max_data = np.nanmax(data, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        normalised = data / max_data[:, np.newaxis]

    normalised[np.isnan(normalised)] = 0

    return normalised
