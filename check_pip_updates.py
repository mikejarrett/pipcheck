#!/usr/bin/env python
# -*- coding: utf8 -*-
import csv
import pip
import xmlrpclib

#update = []
##with open('/tmp/requirements.csv', 'wb') as csvfile:
##    csvwriter = csv.writer(csvfile, delimiter=',')
##    csvwriter.writerow(['Package', 'Current Version', 'Upgrade Avaiable'])
#for dist in pip.get_installed_distributions():
#    available = pypi.package_releases(dist.project_name)
#    if not available:
#        # Try to capitalize pkg name
#        available = pypi.package_releases(dist.project_name.capitalize())
#
#    if not available:
#        msg = 'no releases at pypi'
#    elif available[0] != dist.version:
#        msg = '{} available'.format(available[0])
#        print '{0}={1}'.format(dist.project_name, available[0])
#    else:
#        msg = 'Up To Date'
#
##        name = '{dist.project_name}'.format(dist=dist)
##        version ='{dist.version}'.format(dist=dist)
##        msg = '{msg}'.format(dist=dist, msg=msg)
##        csvwriter.writerow([name, version, msg])


class Checker(object):

    def __init__(self, pypi='http://pypi.python.org/pypi',
                 csv_file='requirements.csv', new_config=None):
        self.pypi = xmlrpclib.ServerProxy(pypi)
        self.csv_file = csv_file
        self.new_config = new_config

    def get_environment_updates(self):
        updates = {}
        for distribution in pip.get_installed_distributions():
            versions = self._get_available_versions(distribution.project_name)

            if versions and max(versions) > distribution.version:
                updates.update({
                    distribution.project_name: {
                        'current': distribution.version,
                        'update': max(versions)}
                })

        return updates



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
