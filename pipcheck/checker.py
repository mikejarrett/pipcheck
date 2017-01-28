# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

import pip as pip_module
from pkg_resources import parse_version

from .clients import PyPIClient
from .constants import UNKNOWN, UNKNOW_NUM, CSV_COLUMN_HEADERS
from .update import Update


class Checker(object):

    def __init__(
        self,
        pypi_client=None,
        pip=None,
        csv_file=False,
        new_config=False,
    ):
        if pypi_client is None:
            pypi_client = PyPIClient()
        self.pypi_client = pypi_client

        if pip is None:
            pip = pip_module
        self.pip = pip

        self._csv_file_name = csv_file
        self._new_config = new_config

    def get_updates(
        self,
        display_all_distributions=False,
        verbose=False
    ):  # pragma: no cover
        """
        When called, get the environment updates and write updates to a CSV
        file and if a new config has been provided, write a new configuration
        file.

        Args:
            display_all_distributions (bool): Return distribution even if it is
                up-to-date.
            verbose (bool): Print to terminal.
        """
        if verbose:
            print('Checking installed packages for updates...')

        updates = self._get_environment_updates(
            display_all_distributions=display_all_distributions
        )

        if updates and verbose:
            for update in updates:
                print(update)

        if updates and self._csv_file_name:
            self.write_updates_to_csv(updates)

        if updates and self._new_config:
            self.write_new_config(updates)

        return updates

    def write_updates_to_csv(self, updates):
        """
        Given a list of updates, write the updates out to the provided CSV
        file.

        Args:
            updates (list): List of Update objects.
        """
        with open(self._csv_file_name, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(CSV_COLUMN_HEADERS)

            for update in updates:
                row = [
                    update.name,
                    update.current_version,
                    update.new_version,
                    update.prelease,
                ]
                csvwriter.writerow(row)

    def write_new_config(self, updates):
        """
        Given a list of updates, write the updates out to the provided
        configuartion file.

        Args:
            updates (list): List of Update objects.
        """
        with open(self._new_config, 'wb') as config_file:
            for update in updates:
                line = '{0}=={1}  # The installed version is: {2}\n'.format(
                    update.name,
                    update.new_version,
                    update.current_version
                )

                config_file.write(line)

    def _get_environment_updates(self, display_all_distributions=False):
        """
        Check all pacakges installed in the environment to see if there are
        any updates availalble.

        Args:
            display_all_distributions (bool): Return distribution even if it is
                up-to-date. Defaults to ``False``.

        Returns:
            list: A list of Update objects ordered based on ``instance.name``.
        """
        updates = []
        for distribution in self.pip.get_installed_distributions():

            versions = self.get_available_versions(distribution.project_name)
            max_version = max(versions.keys()) if versions else UNKNOW_NUM

            update = None
            distribution_version = self._parse_version(distribution.version)
            if versions and max_version > distribution_version:
                update = Update(
                    distribution.project_name,
                    distribution.version,
                    versions[max_version],
                    prelease=max_version[-1]
                )

            elif (
                display_all_distributions and
                max_version == distribution_version
            ):
                update = Update(
                    distribution.project_name,
                    distribution.version,
                    versions[max_version],
                )

            elif display_all_distributions:
                update = Update(
                    distribution.project_name,
                    distribution.version,
                    UNKNOWN
                )

            if update:
                updates.append(update)

        return sorted(updates, key=lambda x: x.name)

    def get_available_versions(self, project_name):
        """ Query PyPI to see if package has any available versions.

        Args:
            project_name (str): The name the project on PyPI.

        Returns:
            dict: Where keys are tuples of parsed versions and values are the
                versions returned by PyPI.
        """
        available_versions = self.pypi_client.package_releases(project_name)

        if not available_versions:
            available_versions = self.pypi_client.package_releases(
                project_name.capitalize()
            )

        # ``dict()`` for Python 2.6 syntax.
        return dict(
            (self._parse_version(version), version)
            for version in available_versions
        )

    @staticmethod
    def _parse_version(version):
        """ Parse a version string.

        Args:
            version (str): A string representing a version e.g. '1.9rc2'

        Returns:
            tuple: major, minor, patch parts cast as integer and whether or not
                it was a pre-release version.
        """
        parsed_version = parse_version(version)
        return tuple(
            int(dot_version)
            for dot_version in parsed_version.base_version.split('.')
        ) + (parsed_version.is_prerelease,)
