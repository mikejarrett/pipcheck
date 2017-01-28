#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys

import pip

from .checker import Checker
from .clients import PyPIClient
from .constants import PYPI_URL


def parse_args(args):
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
        default=PYPI_URL,
        metavar=PYPI_URL,
        nargs='?',
        help='Change the PyPI server from {0}'.format(PYPI_URL),
    )

    return parser.parse_args(args)


def main():  # pragma: no cover
    args = sys.argv[1:]
    if not args:
        args = ['--help']

    args = parse_args(args)

    checker = Checker(
        pypi_client=PyPIClient(args.pypi),
        pip=pip,
        csv_file=args.csv,
        new_config=args.requirements,
    )
    verbose = args.verbose
    if not (args.csv or args.requirements):
        verbose = True

    checker.get_updates(
        display_all_distributions=args.all,
        verbose=verbose
    )
