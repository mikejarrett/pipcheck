# -*- coding: utf-8 -*-
from .constants import PYPI_URL
from .exceptions import PyPIClientError


try:  # Py3
    import xmlrpc.client as xmlrpclib
except ImportError:  # Py2
    import xmlrpclib


class PyPIClient(object):

    def __init__(self, pypi_url=PYPI_URL):
        self._connection = xmlrpclib.ServerProxy(pypi_url)

    def package_releases(self, project_name):
        """ Retrieve the versions from PyPI by ``project_name``.

        Args:
            project_name (str): The name of the project we wish to retrieve
                the versions of.

        Returns:
            list: Of string versions.
        """
        try:
            return self._connection.package_releases(project_name)
        except Exception as err:
            raise PyPIClientError(err)


class PyPIClientPureMemory(object):

    """
    A pure memory implementation of the PyPI client to be used in testing only.

    Attributes:
        packages (dict): A "mocked" PyPI representation.
    """

    packages = {}

    def wipe(self):
        """ Clear ``self.packages``. """
        self.packages = {}

    def package_releases(self, project_name):
        """ Retrieve the versions from ``self.packages`` by ``project_name``.

        Args:
            project_name (str): The name of the project we wish to retrieve
                the versions of.

        Returns:
            list: Of string versions.
        """
        return self.packages.get(project_name, [])

    def set_package_releases(self, project_name, versions):
        """ Storage package information in ``self.packages``

        Args:
            project_name (str): This will be used as a the key in the
                dictionary.
            versions (list): List of ``str`` representing the available
                versions of a project.
        """
        self.packages[project_name] = sorted(versions, reverse=True)
