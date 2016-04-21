# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

import mock as mock_
from unittest2 import TestCase

from pipcheck.pipcheck import Checker
from pipcheck.pipcheck import Update


@mock_.patch('pipcheck.pipcheck.xmlrpclib')
def get_checker(xmlrpclib=None):
    xmlrpclib.ServerProxy.return_value = mock_.Mock()
    return Checker()

if sys.version_info[0] == 3:
    file_spec = ['_CHUNK_SIZE', '__enter__', '__eq__', '__exit__',
        '__format__', '__ge__', '__gt__', '__hash__', '__iter__', '__le__',
        '__lt__', '__ne__', '__next__', '__repr__', '__str__',
        '_checkClosed', '_checkReadable', '_checkSeekable',
        '_checkWritable', 'buffer', 'close', 'closed', 'detach',
        'encoding', 'errors', 'fileno', 'flush', 'isatty',
        'line_buffering', 'mode', 'name',
        'newlines', 'peek', 'raw', 'read', 'read1', 'readable',
        'readinto', 'readline', 'readlines', 'seek', 'seekable', 'tell',
        'truncate', 'writable', 'write', 'writelines']
else:
    file_spec = file

def mock_open(mock=None, data=None):
    if mock is None:
        mock = mock_.MagicMock(spec=file_spec)

    handle = mock_.MagicMock(spec=file_spec)
    handle.write.return_value = None
    if data is None:
        handle.__enter__.return_value = handle
    else:
        handle.__enter__.return_value = data
    mock.return_value = handle
    return mock


class TestChecker(TestCase):

    def test_checker_init(self):
        checker = Checker(csv_file='/path/file.csv', new_config='/path/new.pip')
        self.assertEqual(checker._csv_file, '/path/file.csv')
        self.assertEqual(checker._new_config, '/path/new.pip')


    @mock_.patch('pipcheck.pipcheck.Checker.write_updates_to_csv')
    @mock_.patch('pipcheck.pipcheck.Checker.write_new_config')
    @mock_.patch('pipcheck.pipcheck.Checker._get_environment_updates')
    def test_checker_call_no_verbose(self, get_updates, write_config, write_csv):
        update = mock_.Mock()
        get_updates.return_value = [update]
        Checker(csv_file='/path/file.csv', new_config='/path/new.pip')()

        self.assertEqual(get_updates.call_count, 1)
        self.assertEqual(write_config.call_count, 1)
        self.assertEqual(write_csv.call_count, 1)
        self.assertEqual(write_config.call_args, mock_.call([update]))
        self.assertEqual(write_csv.call_args, mock_.call([update]))

    @mock_.patch('pipcheck.pipcheck.Checker.write_updates_to_csv')
    @mock_.patch('pipcheck.pipcheck.Checker.write_new_config')
    @mock_.patch('pipcheck.pipcheck.Checker._get_environment_updates')
    def test_checker_call_verbose(self, get_updates, write_config, write_csv):
        update = mock_.Mock()
        get_updates.return_value = [update]
        checker = Checker(csv_file='/path/file.csv', new_config='/path/new.pip')
        checker(get_all_updates=True, verbose=True)

        self.assertEqual(get_updates.call_count, 1)
        self.assertEqual(get_updates.call_args, mock_.call(get_all_updates=True))
        self.assertEqual(write_config.call_count, 1)
        self.assertEqual(write_csv.call_count, 1)
        self.assertEqual(write_config.call_args, mock_.call([update]))
        self.assertEqual(write_csv.call_args, mock_.call([update]))


    @mock_.patch('pipcheck.pipcheck.csv')
    def test_write_updates_to_csv(self, patched_csv):
        updates = [Update('First', 1, 2), Update('Last', 5, 9)]
        csv_writer = mock_.Mock()
        patched_csv.writer.return_value = csv_writer

        checker = Checker()
        open_mock = mock_open()
        with mock_.patch('pipcheck.pipcheck.open', open_mock, create=True):
            checker.write_updates_to_csv(updates)

            self.assertEqual(patched_csv.writer.call_args, mock_.call(
                open_mock.return_value, delimiter=','
            ))
            self.assertEqual(patched_csv.writer.call_count, 1)
            self.assertEqual(csv_writer.writerow.call_count, 3)
            self.assertEqual(csv_writer.writerow.call_args_list, [
                mock_.call(['Package', 'Current Version', 'Upgrade Avaiable']),
                mock_.call(['First', 1, 2]),
                mock_.call(['Last', 5, 9])
            ])

    def test_write_new_config(self, ):
        updates = [Update('A Package', 1, 2), Update('Last', 5, 9)]

        checker = Checker(new_config='/path/config.pip')
        open_mock = mock_open()
        with mock_.patch('pipcheck.pipcheck.open', open_mock, create=True):
            checker.write_new_config(updates)
            self.assertEqual(open_mock.call_args, mock_.call('/path/config.pip', 'wb'))
            self.assertEqual(open_mock.return_value.write.call_count, 2)


    # @mock_.patch('pipcheck.pipcheck.pip')
    # def test_check_for_updates(self, pip):
        # dist1 = mock_.Mock(project_name='First Project', version=1.3)
        # dist2 = mock_.Mock(project_name='Last Project', version=0.04)
        # pip.get_installed_distributions.return_value = [dist2, dist1]
        # checker = get_checker()

        # with mock_.patch.object(self, checker, '_get_available_versions') as get_versions:
            # get_versions.return_value = [10.1, 0.04, 1.3]
            # ret_val = checker._get_environment_updates()

            # self.assertEqual(isinstance(ret_val, list), True)
            # self.assertEqual(isinstance(ret_val[0], Update), True)
            # self.assertEqual(ret_val[0].name, 'First Project')

    @mock_.patch('pipcheck.pipcheck.pip')
    def test_check_for_updates_same_revision(self, pip):
        dist1 = mock_.Mock(project_name='First Project', version=1.3)
        pip.get_installed_distributions.return_value = [dist1]
        checker = get_checker()

        with mock_.patch.object(checker, '_get_available_versions') as get_versions:
            get_versions.return_value = [1.3]
            ret_val = checker._get_environment_updates(get_all_updates=True)

            self.assertEqual(isinstance(ret_val, list), True)
            self.assertEqual(isinstance(ret_val[0], Update), True)
            self.assertEqual(ret_val[0].name, 'First Project')

    @mock_.patch('pipcheck.pipcheck.pip')
    def test_check_for_updates_versions_with_letters(self, pip):
        dist1 = mock_.Mock(project_name='First Project', version='1.3a')
        dist2 = mock_.Mock(project_name='Last Project', version='0.04dev')
        pip.get_installed_distributions.return_value = [dist2, dist1]
        checker = get_checker()

        with mock_.patch.object(checker, '_get_available_versions') as get_versions:
            get_versions.return_value = ['10.1c', '0.04prod', '1.3']
            ret_val = checker._get_environment_updates()

            self.assertEqual(isinstance(ret_val, list), True)
            self.assertEqual(isinstance(ret_val[0], Update), True)
            self.assertEqual(ret_val[0].name, 'First Project')
            self.assertEqual(ret_val[0].new_version, '10.1c')

    def test_get_available_versions_capitalize(self):
        package_releases = mock_.Mock(side_effect=([], [1.0]))
        checker = get_checker()
        checker._pypi.package_releases = package_releases

        checker._get_available_versions('distribution')
        self.assertEqual(checker._pypi.package_releases.call_args_list, [
            mock_.call('distribution'), mock_.call('Distribution')])
