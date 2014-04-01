# -*- coding: utf8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Environment package update checker',
    'author': 'Mike Jarrett',
    'url': 'https://github.com/mikejarrett',
    'download_url': 'https://github.com/mikejarrett',
    'author_email': 'mdj00m@gmail.com',
    'version': '0.1a',
    'install_requires': ['nose'],
    'packages': ['pipcheck'],
    'scripts': [],
    'name': 'pip-checker',
    'entry_points':  {
        'console_scripts': [
            'pipcheck = pipcheck.main:main',
        ]
    },
}

setup(**config)
