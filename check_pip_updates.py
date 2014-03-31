#!/usr/bin/env python
import csv
import pip
import xmlrpclib

update = []
pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
#with open('/tmp/requirements.csv', 'wb') as csvfile:
#    csvwriter = csv.writer(csvfile, delimiter=',')
#    csvwriter.writerow(['Package', 'Current Version', 'Upgrade Avaiable'])
for dist in pip.get_installed_distributions():
    available = pypi.package_releases(dist.project_name)
    if not available:
        # Try to capitalize pkg name
        available = pypi.package_releases(dist.project_name.capitalize())

    if not available:
        msg = 'no releases at pypi'
    elif available[0] != dist.version:
        msg = '{} available'.format(available[0])
        print '{0}={1}'.format(dist.project_name, available[0])
    else:
        msg = 'Up To Date'

#        name = '{dist.project_name}'.format(dist=dist)
#        version ='{dist.version}'.format(dist=dist)
#        msg = '{msg}'.format(dist=dist, msg=msg)
#        csvwriter.writerow([name, version, msg])

