# -*- coding: utf8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pipcheck

config = {
    'description': 'Environment package update checker',
    'author': 'Mike Jarrett',
    'url': 'https://github.com/mikejarrett/pipcheck',
    'download_url': 'https://github.com/mikejarrett/pipcheck',
    'author_email': 'mdj00m@gmail.com',
    'version': pipcheck.__version__,
    'install_requires': ['pip'],
    'packages': ['pipcheck'],
    'scripts': [],
    'name': 'pipcheck',
    'entry_points':  {
        'console_scripts': [
            'pipcheck = pipcheck.main:main',
        ]
    },
}

setup(**config)
