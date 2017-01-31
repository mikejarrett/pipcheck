# -*- coding: utf-8 -*-
import argparse

from pipcheck.constants import PYPI_URL


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
