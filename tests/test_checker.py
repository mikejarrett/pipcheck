# -*- coding: utf8 -*-
import mock

from nose.tools import eq_ as assert_equals

from pipcheck.pipcheck import Checker, Update


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
    checker = get_checker()
    assert_equals(checker.csv_file, 'requirements.csv')
    assert_equals(checker.new_config, None)


@mock.patch('pipcheck.pipcheck.csv')
@mock.patch('pipcheck.pipcheck.Checker.get_environment_updates')
def test_write_updates_to_csv(get_updates, patched_csv):
    get_updates.return_value = [Update('First', 1, 2), Update('Last', 5, 9)]
    csv_writer = mock.Mock()
    patched_csv.writer.return_value = csv_writer

    checker = Checker()
    open_mock = mock_open()
    with mock.patch('pipcheck.pipcheck.open', open_mock, create=True):
        checker.write_updates_to_csv()

        assert_equals(get_updates.call_count, 1)
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


@mock.patch('pipcheck.pipcheck.pip')
def test_check_for_updates(pip):
    dist1 = mock.Mock(project_name='First Project', version=1.3)
    dist2 = mock.Mock(project_name='Last Project', version=0.04)
    pip.get_installed_distributions.return_value = [dist2, dist1]
    checker = get_checker()

    with mock.patch.object(checker, '_get_available_versions') as get_versions:
        get_versions.return_value = [10.1, 0.04, 1.3]
        ret_val = checker.get_environment_updates()

        assert_equals(isinstance(ret_val, list), True)
        assert_equals(isinstance(ret_val[0], Update), True)
        assert_equals(ret_val[0].name, 'First Project')


def test_get_available_versions_capitalize():
    package_releases = mock.Mock(side_effect=([], [1.0]))
    checker = get_checker()
    checker.pypi.package_releases = package_releases

    checker._get_available_versions('distribution')
    assert_equals(checker.pypi.package_releases.call_args_list, [
        mock.call('distribution'), mock.call('Distribution')])
