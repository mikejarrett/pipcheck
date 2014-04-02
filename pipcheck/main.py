#!/usr/bin/env python
# -*- coding: utf8 -*-
import argparse

from pipcheck import Checker

def main():
    parser = argparse.ArgumentParser(
        description='pipcheck is an application that checks for updates for '
                    'PIP packages that are installed'
    )
    parser.add_argument('-c', '--csv', nargs='?', metavar='/path/file',
                        help='Define a location for csv output')
    parser.add_argument(
        '-r', '--requirements', nargs='?', metavar='/path/file',
        help='Define location for new requirements file output')
    parser.add_argument(
        '-p', '--pypi', nargs='?',
        help='Change the pypi server from http://pypi.python.org/pypi',
        default='http://pypi.python.org/pypi',
        metavar='http://pypi.python.org/pypi'
    )

    args = parser.parse_args()
    if not (args.csv or args.requirements):
        parser.error('Need one of either --csv or --requirements')

    Checker(csv_file=args.csv, new_config=args.requirements, pypi=args.pypi)()
