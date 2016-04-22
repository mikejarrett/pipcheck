# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from future.utils import python_2_unicode_compatible

import csv
try:  # Py3
   import xmlrpc.client as xmlrpclib
except ImportError:  # Py2
    import xmlrpclib

import pip


UNKNOWN = 'Unknown'
UNKNOW_NUM = -32768


@python_2_unicode_compatible
class Update(object):

    @property
    def up_to_date(self):
        return self.current_version == self.new_version

    def __init__(self, name, current_version, new_version):
        self.name = name
        self.current_version = current_version
        self.new_version = new_version

    def __str__(self):
        if self.up_to_date:
            return u'Update {name} (up to date)'.format(name=self.name)
        elif self.new_version == UNKNOWN:
            return u'Update {name} ({new_version})'.format(
                name=self.name, new_version=self.new_version)
        else:
            return (
                u'Update {name} ({current_version} to '
                u'{new_version})'.format(
                    name=self.name, current_version=self.current_version,
                    new_version=self.new_version
                ))

    def __repr__(self):
        return str(self)

        
class Checker(object):

    def __init__(
        self,
        csv_file=False,
        new_config=False,
        pypi='http://pypi.python.org/pypi'
    ):
        self._pypi = xmlrpclib.ServerProxy(pypi)
        self._csv_file = csv_file
        self._new_config = new_config
        self._csv_column_headers = [
            'Package', 'Current Version', 'Upgrade Avaiable'
        ]

    def __call__(self, get_all_updates=False, verbose=False):
        """
        When called, get the environment updates and write updates to a CSV
        file and if a new config has been provided, write a new configuration
        file.
        """
        print('Checking installed packages for updates...')
        updates = self._get_environment_updates(
            get_all_updates=get_all_updates)

        if updates and verbose:
            for update in updates:
                print(update)

        if updates and self._csv_file:
            self.write_updates_to_csv(updates)

        if updates and self._new_config:
            self.write_new_config(updates)

    def write_updates_to_csv(self, updates):
        """
        Given a list of updates, write the updates out to the provided CSV file

        :param updates: List of Update objects
        :param type: list
        """
        with open(self._csv_file, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(self._csv_column_headers)

            for update in updates:
                row = [update.name, update.current_version, update.new_version]
                csvwriter.writerow(row)

    def write_new_config(self, updates):
        """
        Given a list of updates, write the updates out to the provided
        configuartion file

        :param updates: List of Update objects
        :param type: list
        """
        with open(self._new_config, 'wb') as config_file:
            for update in updates:
                line = '{0}=={1} # The current version is: {2}\n'.format(
                update.name, update.new_version, update.current_version)

                config_file.write(line)

    def _get_environment_updates(self, get_all_updates=False):
        """
        Check all pacakges installed in the environment to see if there are
        any updates availalble

        :returns: A list of Update objects ordered based on instance.name
        :rtype: list
        """
        updates = []
        for distribution in pip.get_installed_distributions():
            versions = self._get_available_versions(distribution.project_name)

            max_version = max(versions) if versions else UNKNOW_NUM
            if versions and max_version > distribution.version:
                updates.append(Update(
                    distribution.project_name, distribution.version,
                    max_version
                ))
            elif get_all_updates and max_version == distribution.version:
                updates.append(Update(
                    distribution.project_name, distribution.version,
                    max_version
                ))
            elif get_all_updates:
                updates.append(Update(
                    distribution.project_name, distribution.version, UNKNOWN
                ))

        return sorted(updates, key=lambda x: x.name)

    def _get_available_versions(self, project_name):
        """ Query pypi to see if package has any available versions.r

        :param project_name: The name of the project on pypi
        :type project_name: str
        :returns: list of float versions
        :rtype: list of float
        """
        available_versions = self._pypi.package_releases(project_name)
        if not available_versions:
            available_versions = self._pypi.package_releases(
                project_name.capitalize()
            )

        return available_versions
