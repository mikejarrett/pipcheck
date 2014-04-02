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

import mock

from nose.tools import eq_ as assert_equals

from pipcheck.pipcheck import Checker
from pipcheck.pipcheck import Update


@mock.patch('pipcheck.pipcheck.xmlrpclib')
def get_checker(xmlrpclib=None):
    xmlrpclib.ServerProxy.return_value = mock.Mock()
    return Checker()


def mock_open(mck=None, data=None):
    file_spec = file

    if mck is None:
        mck = mock.MagicMock(spec=file_spec)

    handle = mock.MagicMock(spec=file_spec)
    handle.write.return_value = None
    if data is None:
        handle.__enter__.return_value = handle
    else:
        handle.__enter__.return_value = data
    mck.return_value = handle
    return mck


def test_checker_init():
    checker = Checker(csv_file='/path/file.csv', new_config='/path/new.pip')
    assert_equals(checker._csv_file, '/path/file.csv')
    assert_equals(checker._new_config, '/path/new.pip')


@mock.patch('pipcheck.pipcheck.Checker.write_updates_to_csv')
@mock.patch('pipcheck.pipcheck.Checker.write_new_config')
@mock.patch('pipcheck.pipcheck.Checker._get_environment_updates')
def test_checker_call(get_updates, write_config, write_csv):
    update = mock.Mock()
    get_updates.return_value = [update]
    Checker(csv_file='/path/file.csv', new_config='/path/new.pip')()

    assert_equals(get_updates.call_count, 1)
    assert_equals(write_config.call_count, 1)
    assert_equals(write_csv.call_count, 1)
    assert_equals(write_config.call_args, mock.call([update]))
    assert_equals(write_csv.call_args, mock.call([update]))


@mock.patch('pipcheck.pipcheck.csv')
def test_write_updates_to_csv(patched_csv):
    updates = [Update('First', 1, 2), Update('Last', 5, 9)]
    csv_writer = mock.Mock()
    patched_csv.writer.return_value = csv_writer

    checker = Checker()
    open_mock = mock_open()
    with mock.patch('pipcheck.pipcheck.open', open_mock, create=True):
        checker.write_updates_to_csv(updates)

        assert_equals(patched_csv.writer.call_args, mock.call(
            open_mock.return_value, delimiter=','
        ))
        assert_equals(patched_csv.writer.call_count, 1)
        assert_equals(csv_writer.writerow.call_count, 3)
        assert_equals(csv_writer.writerow.call_args_list, [
            mock.call(['Package', 'Current Version', 'Upgrade Avaiable']),
            mock.call(['First', 1, 2]),
            mock.call(['Last', 5, 9])
        ])

def test_write_new_config():
    updates = [Update('A Package', 1, 2), Update('Last', 5, 9)]

    checker = Checker(new_config='/path/config.pip')
    open_mock = mock_open()
    with mock.patch('pipcheck.pipcheck.open', open_mock, create=True):
        checker.write_new_config(updates)
        assert_equals(open_mock.call_args, mock.call('/path/config.pip', 'wb'))
        assert_equals(open_mock.return_value.write.call_count, 2)


@mock.patch('pipcheck.pipcheck.pip')
def test_check_for_updates(pip):
    dist1 = mock.Mock(project_name='First Project', version=1.3)
    dist2 = mock.Mock(project_name='Last Project', version=0.04)
    pip.get_installed_distributions.return_value = [dist2, dist1]
    checker = get_checker()

    with mock.patch.object(checker, '_get_available_versions') as get_versions:
        get_versions.return_value = [10.1, 0.04, 1.3]
        ret_val = checker._get_environment_updates()

        assert_equals(isinstance(ret_val, list), True)
        assert_equals(isinstance(ret_val[0], Update), True)
        assert_equals(ret_val[0].name, 'First Project')


def test_get_available_versions_capitalize():
    package_releases = mock.Mock(side_effect=([], [1.0]))
    checker = get_checker()
    checker._pypi.package_releases = package_releases

    checker._get_available_versions('distribution')
    assert_equals(checker._pypi.package_releases.call_args_list, [
        mock.call('distribution'), mock.call('Distribution')])
