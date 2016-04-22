#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from .pipcheck import Checker


def main():
    parser = argparse.ArgumentParser(
        description=(
            'pipcheck is an application that checks for updates for PIP '
            'packages that are installed.'
        )
    )
    parser.add_argument(
        '-c',
        '--csv',
        metavar='/path/file',
        nargs='?',
        help='Define a location for csv output'
    )
    parser.add_argument(
        '-r',
        '--requirements',
        nargs='?',
        metavar='/path/file',
        help='Define location for new requirements file output'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Display the status of updates of packages'
    )
    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        help='Returns results for all installed packages'
    )
    parser.add_argument(
        '-p',
        '--pypi',
        default='http://pypi.python.org/pypi',
        metavar='http://pypi.python.org/pypi',
        nargs='?',
        help='Change the pypi server from http://pypi.python.org/pypi',
    )

    args = parser.parse_args()
    checker = Checker(
        csv_file=args.csv,
        new_config=args.requirements,
        pypi=args.pypi
    )
    verbose = args.verbose
    if not (args.csv or args.requirements):
        verbose = True

    checker(get_all_updates=args.all, verbose=verbose)
