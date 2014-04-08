#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2014 Mike Jarrett
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

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
        '-v', '--verbose', action='store_true',
        help='Display the status of updates of packages')
    parser.add_argument(
        '-a', '--all', action='store_true',
        help='Returns results for all installed packages')
    parser.add_argument(
        '-p', '--pypi', nargs='?',
        help='Change the pypi server from http://pypi.python.org/pypi',
        default='http://pypi.python.org/pypi',
        metavar='http://pypi.python.org/pypi'
    )

    args = parser.parse_args()
    checker = Checker(
        csv_file=args.csv, new_config=args.requirements, pypi=args.pypi
    )
    verbose = args.verbose
    if not (args.csv or args.requirements):
        verbose = True
    checker(get_all_updates=args.all, verbose=verbose)
