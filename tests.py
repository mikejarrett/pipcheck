# -*- coding: utf8 -*-
import mock

from nose.tools import eq_ as assert_equals

from check_pip_updates import Checker


@mock.patch('check_pip_updates.xmlrpclib')
def get_checker(xmlrpclib):
    xmlrpclib.ServerProxy.return_value = mock.Mock()
    return Checker()

def test_init():
    checker = get_checker()

    assert_equals(checker.csv_file, 'requirements.csv')
    assert_equals(checker.new_config, None)

@mock.patch('check_pip_updates.pip')
def test_check_for_updates(pip):
    dist1 = mock.Mock(project_name='Project Name', version=1.3)
    dist2 = mock.Mock(project_name='Another Project', version=0.04)
    pip.get_installed_distributions.return_value = [dist1, dist2]
    checker = get_checker()

    with mock.patch.object(checker, '_get_available_versions') as get_versions:
        get_versions.return_value = [10.1, 0.04, 1.3]
        ret_val = checker.get_environment_updates()

        assert_equals(ret_val['Project Name'], {
            'current': 1.3, 'update': 10.1})
        assert_equals(get_versions.call_count, 2)


def test_get_available_versions_capitalize():
    package_releases = mock.Mock(side_effect=([], [1.0]))
    checker = get_checker()
    checker.pypi.package_releases = package_releases

    checker._get_available_versions('distribution')
    assert_equals(checker.pypi.package_releases.call_args_list, [
        mock.call('distribution'), mock.call('Distribution')])
