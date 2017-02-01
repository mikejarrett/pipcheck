# -*- coding: utf-8 -*-
# pylint: disable=protected-access
import sys
import types
from collections import namedtuple

import pip
import mock
from unittest2 import TestCase

from pipcheck.checker import Checker
from pipcheck.clients import PyPIClientPureMemory, PyPIClient
from pipcheck.constants import UNKNOWN, CSV_COLUMN_HEADERS
from pipcheck.update import Update


Distribution = namedtuple('Distribution', ['project_name', 'version'])


# Mock ``open`` and file``
if sys.version_info[0] == 3:  # Python 3+
    # pylint: disable=invalid-name
    FILE_SPEC = [
        '_CHUNK_SIZE',
        '__enter__',
        '__eq__',
        '__exit__',
        '__format__',
        '__ge__',
        '__gt__',
        '__hash__',
        '__iter__',
        '__le__',
        '__lt__',
        '__ne__',
        '__next__',
        '__repr__',
        '__str__',
        '_checkClosed',
        '_checkReadable',
        '_checkSeekable',
        '_checkWritable',
        'buffer',
        'close',
        'closed',
        'detach',
        'encoding',
        'errors',
        'fileno',
        'flush',
        'isatty',
        'line_buffering',
        'mode',
        'name',
        'newlines',
        'peek',
        'raw',
        'read',
        'read1',
        'readable',
        'readinto',
        'readline',
        'readlines',
        'seek',
        'seekable',
        'tell',
        'truncate',
        'writable',
        'write',
        'writelines'
    ]

else:  # Python 2
    # pylint: disable=redefined-variable-type,invalid-name,undefined-variable
    FILE_SPEC = file  # pylint: disable=undefined-variable


def mockopen(mocker=None, data=None):
    if mocker is None:
        mocker = mock.MagicMock(spec=FILE_SPEC)

    handle = mock.MagicMock(spec=FILE_SPEC)
    handle.write.return_value = None
    if data is None:
        handle.__enter__.return_value = handle
    else:
        handle.__enter__.return_value = data

    mocker.return_value = handle
    return mocker


class PipMock(object):

    def __init__(self):
        self.distributions = []

    def set_installed_distributions(self, distributions):
        """
            Args:
                distributions (list): A list of "``distributions``".
        """
        assert isinstance(distributions, (tuple, list))
        self.distributions = distributions

    def get_installed_distributions(self):
        return self.distributions


class TestChecker(TestCase):

    maxDiff = None
    pypi_client = PyPIClientPureMemory()

    def setUp(self):
        self.pypi_client.set_package_releases(
            'pipcheck',
            ['0.0.1', '0.0.2', '0.0.3', '0.0.4', '0.0.5', '0.0.6'],
        )

    def tearDown(self):
        self.pypi_client.wipe()

    def test_get_updates_no_updates_available(self):
        checker = Checker(
            pypi_client=self.pypi_client,
            pip=PipMock(),
        )

        actual = checker.get_updates()
        self.assertEqual(actual, [])

    def test_get_updates_updates_available(self):
        pip_ = PipMock()
        pip_.set_installed_distributions([Distribution('pipcheck', '0.0.1')])

        checker = Checker(
            pypi_client=self.pypi_client,
            pip=pip_,
        )

        actual = checker.get_updates()
        expected = [Update('pipcheck', '0.0.1', '0.0.6')]
        self.assertEqual(actual, expected)

    def test_get_updates_updates_available_prerelease(self):
        self.pypi_client.set_package_releases('Pipcheck', ['0.0.6rc1'])

        pip_ = PipMock()
        pip_.set_installed_distributions(
            [Distribution('Pipcheck', '0.0.1')]
        )

        checker = Checker(
            pypi_client=self.pypi_client,
            pip=pip_,
        )

        actual = checker.get_updates()
        expected = [Update('Pipcheck', '0.0.1', '0.0.6rc1', True)]
        self.assertEqual(actual, expected)

    def test_get_updates_display_all_distributions(self):
        pip_ = PipMock()
        pip_.set_installed_distributions(
            [Distribution('pipcheck', '0.0.6')]
        )

        checker = Checker(
            pypi_client=self.pypi_client,
            pip=pip_,
        )

        actual = checker.get_updates(display_all_distributions=True)
        expected = [Update('pipcheck', '0.0.6', '0.0.6', False)]
        self.assertEqual(actual, expected)

    def test_get_updates_display_all_distributions_multiple(self):
        pip_ = PipMock()
        pip_.set_installed_distributions([
            Distribution('pipcheck', '0.0.6'),
            Distribution('flush', '1.8.6')
        ])

        checker = Checker(
            pypi_client=self.pypi_client,
            pip=pip_,
        )

        actual = checker.get_updates(display_all_distributions=True)
        expected = [
            Update('flush', '1.8.6', UNKNOWN, False),
            Update('pipcheck', '0.0.6', '0.0.6', False)
        ]
        self.assertEqual(actual, expected)

    @mock.patch('pipcheck.checker.csv')
    def test_write_updates_to_csv(self, patched_csv):
        updates = [Update('First', 1, 2), Update('Last', 5, 9)]

        csv_writer = mock.Mock()
        patched_csv.writer.return_value = csv_writer

        pip_ = PipMock()
        checker = Checker(
            pypi_client=self.pypi_client,
            pip=pip_,
        )

        open_mock = mockopen()
        with mock.patch('pipcheck.checker.open', open_mock, create=True):
            checker.write_updates_to_csv(updates)

        if sys.version_info >= (3,):
            expected = mock.call(
                open_mock.return_value,
                delimiter=',',
                lineterminator='\n'
            )
        else:
            expected = mock.call(
                open_mock.return_value,
                delimiter=b',',
                lineterminator='\n'
            )

        self.assertEqual(
            patched_csv.writer.call_args,
            expected
        )
        self.assertEqual(patched_csv.writer.call_count, 1)
        self.assertEqual(csv_writer.writerow.call_count, 3)
        self.assertEqual(
            csv_writer.writerow.call_args_list,
            [
                mock.call(CSV_COLUMN_HEADERS),
                mock.call(['First', 1, 2, False]),
                mock.call(['Last', 5, 9, False])
            ]
        )

    def test_write_new_config(self):
        updates = [Update('A Package', 1, 2), Update('Last', 5, 9)]

        pip_ = PipMock()
        checker = Checker(
            pypi_client=self.pypi_client,
            pip=pip_,
            new_config='/path/config.pip'
        )
        open_mock = mockopen()
        with mock.patch('pipcheck.checker.open', open_mock, create=True):
            checker.write_new_config(updates)

        self.assertEqual(
            open_mock.call_args,
            mock.call('/path/config.pip', 'w')
        )
        self.assertEqual(open_mock.return_value.write.call_count, 2)

    def test_init(self):
        checker = Checker()
        self.assertTrue(isinstance(checker.pypi_client, PyPIClient))
        self.assertTrue(isinstance(checker.pip, types.ModuleType))
        self.assertTrue(checker.pip.__name__, pip.__name__)
        self.assertFalse(checker._csv_file_name)
        self.assertFalse(checker._new_config)
