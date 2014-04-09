# -*- coding: utf8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pipcheck


with open('README.rst', 'rb') as readme:
    long_description = readme.read()


config = {
    'name': 'pipcheck',
    'version': pipcheck.__version__,
    'author': 'Mike Jarrett',
    'author_email': 'mdj00m@gmail.com',
    'url': 'https://github.com/mikejarrett/pipcheck',
    'description': 'Environment package update checker',
    'long_description': long_description,
    'download_url': 'https://github.com/mikejarrett/pipcheck',
    'install_requires': ['pip'],
    'packages': ['pipcheck'],
    'scripts': [],
    'entry_points':  {
        'console_scripts': [
            'pipcheck = pipcheck.main:main',
        ]},
}

setup(**config)
