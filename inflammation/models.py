"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains 
inflammation data for a single patient taken over a number of days 
and each column represents a single day across all patients.
"""
import glob
import json
import os

import numpy as np

class CSVDataSource:

    def __init__(self, data_dir):
        self.data_dir = data_dir

    @staticmethod
    def load_csv(filename):
        """Load a Numpy array from a CSV

        :param filename: Filename of CSV to load
        """
        return np.loadtxt(fname=filename, delimiter=',')

    def load_inflammation_data(self):
        data_file_paths = glob.glob(os.path.join(self.data_dir, 'inflammation*.csv'))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation data CSV files found in path {self.data_dir}")
        data = map(self.load_csv, data_file_paths)
        return data


class JSONDataSource:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    @staticmethod
    def load_json(filename):
        """Load a numpy array from a JSON document.

        Expected format:
        [
            {
                observations: [0, 1]
            },
            {
                observations: [0, 2]
            }
        ]

        :param filename: Filename of CSV to load

        """
        with open(filename, 'r', encoding='utf-8') as file:
            data_as_json = json.load(file)
            return [np.array(entry['observations']) for entry in data_as_json]

    def load_inflammation_data(self):
        data_file_paths = glob.glob(os.path.join(self.data_dir, '*.csv'))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation data JSON files found in path {self.data_dir}")
        data = map(self.load_json, data_file_paths)
        return data


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




def compute_stddev_by_day(data):
    means_by_day = map(daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))
    daily_standard_deviation = np.std(means_by_day_matrix, axis=0)
    return daily_standard_deviation


def analyse_data(data_source):
    """Calculates the standard deviation by day between datasets.

    Gets all the inflammation data from CSV files within a directory,
    works out the mean inflammation value for each day across all datasets,
    then plots the graphs of standard deviation of these means."""

    data = data_source.load_inflammation_data()

    daily_standard_deviation = compute_stddev_by_day(data)

    return daily_standard_deviation