#!/usr/bin/env python
# -*- coding: utf8 -*-
import csv
import pip
import xmlrpclib


class Update(object):

    def __init__(self, name, current_version, new_version):
        self.name = name
        self.current_version = current_version
        self.new_version = new_version

    def __repr__(self):
        return u'<Update {0} ({1} to {2})>'.format(
            self.name, self.current_version, self.new_version)

    def __str__(self):
        return u'Update {0} ({1} to {2})'.format(
            self.name, self.current_version, self.new_version)


class Checker(object):

    def __init__(self, pypi='http://pypi.python.org/pypi',
                 csv_file='requirements.csv', new_config=None):
        self.pypi = xmlrpclib.ServerProxy(pypi)
        self.csv_file = csv_file
        self.new_config = new_config
        self.csv_column_headers = [
            'Package', 'Current Version', 'Upgrade Avaiable'
        ]

    def write_updates_to_csv(self):
        """
        Checks for package updates and writes the returned dictionary to CSV
        file defined at init
        """
        updates = self.get_environment_updates()

        with open(self.csv_file, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(self.csv_column_headers)

            for update in updates:
                row = [update.name, update.current_version, update.new_version]
                csvwriter.writerow(row)

    def get_environment_updates(self):
        """
        Check all pacakges installed in the environment to see if there are
        any updates availalble

        :returns: A list of Update objects ordered based on instance.name
        :rtype: list
        """
        updates = []
        for distribution in pip.get_installed_distributions():
            versions = self._get_available_versions(distribution.project_name)

            if versions and max(versions) > distribution.version:
                updates.append(Update(
                    distribution.project_name, distribution.version,
                    max(versions)
                ))

        return sorted(updates, key=lambda x: x.name)

    def _get_available_versions(self, project_name):
        """ Query pypi to see if package has any available versions.r

        :param project_name: The name of the project on pypi
        :type project_name: str
        :returns: list of float versions
        :rtype: list of float
        """
        available_versions = self.pypi.package_releases(project_name)
        if not available_versions:
            available_versions = self.pypi.package_releases(
                project_name.capitalize()
            )

        return available_versions
