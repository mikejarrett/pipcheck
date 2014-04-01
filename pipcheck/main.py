#!/usr/bin/env python
# -*- coding: utf8 -*-
import argparse

from pipcheck import Checker

def main():
    parser = argparse.ArgumentParser(
        description='pipcheck checks the pip install packages of your '
        'environment for updates')
    parser.add_argument('-c', '--csv', nargs='?', metavar='path/FILE',
                        help='Define a location for csv output')
    parser.add_argument(
        '-r', '--requirements', metavar='path/FILE',
        help='Define location for new requirements file output')

    args = parser.parse_args()
    Checker(csv_file=args.csv, new_config=args.requirements)()


if __name__ == '__main__':
    main()
