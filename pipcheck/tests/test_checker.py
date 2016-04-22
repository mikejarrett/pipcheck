# -*- coding: utf-8 -*-
# pylint: disable=protected-access
from __future__ import unicode_literals
import sys

import mock

from unittest2 import TestCase

from pipcheck.pipcheck import Checker
from pipcheck.pipcheck import Update


@mock.patch('pipcheck.pipcheck.xmlrpclib')
def get_checker(xmlrpclib=None):
    xmlrpclib.ServerProxy.return_value = mock.Mock()
    return Checker()


if sys.version_info[0] == 3:  # Py3
    FILE_SPEC = [  # pylint: disable=invalid-name
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
else:  # Py2
    FILE_SPEC = file  # pylint: disable=redefined-variable-type,invalid-name


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


class TestChecker(TestCase):

    def test_checker_init(self):
        checker = Checker(
            csv_file='/path/file.csv',
            new_config='/path/new.pip'
        )
        self.assertEqual(checker._csv_file, '/path/file.csv')
        self.assertEqual(checker._new_config, '/path/new.pip')

    @mock.patch('pipcheck.pipcheck.Checker.write_updates_to_csv')
    @mock.patch('pipcheck.pipcheck.Checker.write_new_config')
    @mock.patch('pipcheck.pipcheck.Checker._get_environment_updates')
    def test_checker_call_no_verbose(
        self,
        get_updates,
        write_config,
        write_csv
    ):
        update = mock.Mock()
        get_updates.return_value = [update]
        Checker(csv_file='/path/file.csv', new_config='/path/new.pip')()

        self.assertEqual(get_updates.call_count, 1)
        self.assertEqual(write_config.call_count, 1)
        self.assertEqual(write_csv.call_count, 1)
        self.assertEqual(write_config.call_args, mock.call([update]))
        self.assertEqual(write_csv.call_args, mock.call([update]))

    @mock.patch('pipcheck.pipcheck.Checker.write_updates_to_csv')
    @mock.patch('pipcheck.pipcheck.Checker.write_new_config')
    @mock.patch('pipcheck.pipcheck.Checker._get_environment_updates')
    def test_checker_call_verbose(self, get_updates, write_config, write_csv):
        update = mock.Mock()
        get_updates.return_value = [update]
        checker = Checker(
            csv_file='/path/file.csv',
            new_config='/path/new.pip'
        )
        checker(get_all_updates=True, verbose=True)

        self.assertEqual(get_updates.call_count, 1)
        self.assertEqual(
            get_updates.call_args,
            mock.call(get_all_updates=True)
        )
        self.assertEqual(write_config.call_count, 1)
        self.assertEqual(write_csv.call_count, 1)
        self.assertEqual(write_config.call_args, mock.call([update]))
        self.assertEqual(write_csv.call_args, mock.call([update]))

    @mock.patch('pipcheck.pipcheck.csv')
    def test_write_updates_to_csv(self, patched_csv):
        updates = [Update('First', 1, 2), Update('Last', 5, 9)]
        csv_writer = mock.Mock()
        patched_csv.writer.return_value = csv_writer

        checker = Checker()
        open_mock = mockopen()
        with mock.patch('pipcheck.pipcheck.open', open_mock, create=True):
            checker.write_updates_to_csv(updates)

        self.assertEqual(
            patched_csv.writer.call_args,
            mock.call(open_mock.return_value, delimiter=',')
        )
        self.assertEqual(patched_csv.writer.call_count, 1)
        self.assertEqual(csv_writer.writerow.call_count, 3)
        self.assertEqual(
            csv_writer.writerow.call_args_list,
            [
                mock.call(
                    ['Package', 'Current Version', 'Upgrade Avaiable']
                ),
                mock.call(['First', 1, 2]),
                mock.call(['Last', 5, 9])
            ]
        )

    def test_write_new_config(self):
        updates = [Update('A Package', 1, 2), Update('Last', 5, 9)]

        checker = Checker(new_config='/path/config.pip')
        open_mock = mockopen()
        with mock.patch('pipcheck.pipcheck.open', open_mock, create=True):
            checker.write_new_config(updates)

        self.assertEqual(
            open_mock.call_args,
            mock.call('/path/config.pip', 'wb')
        )
        self.assertEqual(open_mock.return_value.write.call_count, 2)

    @mock.patch('pipcheck.pipcheck.pip')
    def test_check_for_updates(self, pip):
        dist1 = mock.Mock(project_name='First Project', version=1.3)
        dist2 = mock.Mock(project_name='Last Project', version=0.04)
        pip.get_installed_distributions.return_value = [dist2, dist1]
        checker = get_checker()

        with mock.patch.object(
            checker,
            '_get_available_versions',
            mock.Mock(return_value=[10.1, 0.04, 1.3])
        ):
            ret_val = checker._get_environment_updates()

        self.assertEqual(isinstance(ret_val, list), True)
        self.assertEqual(isinstance(ret_val[0], Update), True)
        self.assertEqual(ret_val[0].name, 'First Project')

    @mock.patch('pipcheck.pipcheck.pip')
    def test_check_for_updates_same_revision(self, pip):
        dist1 = mock.Mock(project_name='First Project', version=1.3)
        pip.get_installed_distributions.return_value = [dist1]
        checker = get_checker()

        with mock.patch.object(
            checker,
            '_get_available_versions',
            mock.Mock(return_value=[1.3])
        ):
            ret_val = checker._get_environment_updates(get_all_updates=True)

        self.assertTrue(isinstance(ret_val, list))
        self.assertTrue(isinstance(ret_val[0], Update))
        self.assertEqual(ret_val[0].name, 'First Project')

    @mock.patch('pipcheck.pipcheck.pip')
    def test_check_for_updates_versions_with_letters(self, pip):
        dist1 = mock.Mock(project_name='First Project', version='1.3a')
        dist2 = mock.Mock(project_name='Last Project', version='0.04dev')
        pip.get_installed_distributions.return_value = [dist2, dist1]
        checker = get_checker()

        with mock.patch.object(
            checker,
            '_get_available_versions',
            mock.Mock(return_value=['10.1c', '0.04prod', '1.3'])
        ):
            ret_val = checker._get_environment_updates()

        self.assertTrue(isinstance(ret_val, list))
        self.assertTrue(isinstance(ret_val[0], Update))
        self.assertEqual(ret_val[0].name, 'First Project')
        self.assertEqual(ret_val[0].new_version, '10.1c')

    def test_get_available_versions_capitalize(self):
        package_releases = mock.Mock(side_effect=([], [1.0]))
        checker = get_checker()
        checker._pypi.package_releases = package_releases

        checker._get_available_versions('distribution')
        self.assertEqual(
            checker._pypi.package_releases.call_args_list,
            [mock.call('distribution'), mock.call('Distribution')]
        )
