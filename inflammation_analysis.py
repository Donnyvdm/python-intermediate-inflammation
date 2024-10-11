#!/usr/bin/env python3
"""Software for managing and analysing patients' inflammation data in our imaginary hospital."""

import argparse
import os

from inflammation import models, views
from inflammation.models import CSVDataSource, JSONDataSource, analyse_data


def main(args):
    """The MVC Controller of the patient inflammation data system.

    The Controller is responsible for:
    - selecting the necessary models and views for the current task
    - passing data between models and views
    """
    infiles = args.infiles
    if not isinstance(infiles, list):
        infiles = [args.infiles]

    if args.full_data_analysis:
        data_dir = os.path.dirname(infiles[0])

        if infiles[0].endswith('csv'):
            data_source = CSVDataSource(data_dir)
        elif infiles[0].endswith('json'):
            data_source = JSONDataSource(data_dir)
        else:
            raise ValueError(f"Don't know how to load files of type {infiles[0]}")

        data_result = analyse_data(data_source)
        graph_data = {
            'standard deviation by day': data_result,
        }

        views.visualize(graph_data)

        return

    for filename in infiles:
        inflammation_data = models.CSVDataSource.load_csv(filename)

        view_data = {
            'average': models.daily_mean(inflammation_data),
            'max': models.daily_max(inflammation_data),
            'min': models.daily_min(inflammation_data)
        }

        views.visualize(view_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A basic patient inflammation data management system')

    parser.add_argument(
        'infiles',
        nargs='+',
        help='Input CSV(s) containing inflammation series for each patient')

    parser.add_argument(
        '--full-data-analysis',
        action='store_true',
        dest='full_data_analysis')

    args = parser.parse_args()

    main(args)
