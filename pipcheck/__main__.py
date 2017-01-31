#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import pip

from pipcheck.arg_parser import parse_args
from pipcheck.checker import Checker
from pipcheck.clients import PyPIClient


def main(args=None):  # pragma: no cover
    if args is None:
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


if __name__ == '__main__':
    main()
