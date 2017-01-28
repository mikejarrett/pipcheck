# -*- coding: utf-8 -*-
from unittest2 import TestCase

from argparse import Namespace

from pipcheck.main import parse_args
from pipcheck.constants import PYPI_URL


class TestArgParser(TestCase):

    def test_parse_args_empty(self):
        actual = parse_args([])
        expected = Namespace(
            all=False,
            csv=None,
            pypi=PYPI_URL,
            requirements=None,
            verbose=False,
        )
        self.assertEqual(actual, expected)

    def test_parse_args_set_all(self):
        csv_file = '/tmp/file.csv'
        requirements_file = '/tmp/requirements.txt'
        pypi_url = 'http://www.example.com/pypi'

        args = (
            '-c', csv_file,
            '-r', requirements_file,
            '-v',
            '-a',
            '-p', pypi_url,
        )

        actual = parse_args(args)
        expected = Namespace(
            all=True,
            csv=csv_file,
            pypi=pypi_url,
            requirements=requirements_file,
            verbose=True,
        )

        self.assertEqual(actual, expected)
