# -*- coding: utf8 -*-
from codecs import open
from os import path

from setuptools import setup

import pipcheck


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as file_:
    long_description = file_.read()


setup(
    name='pipcheck',
    version=pipcheck.__version__,
    author='Mike Jarrett',
    author_emai='mike<dot>d<dot>jarrett<at>gmail<dot>com',
    url='https://github.com/mikejarrett/pipcheck',
    description='Environment package update checker',
    long_description=long_description,
    download_url='https://github.com/mikejarrett/pipcheck',
    install_requires=['pip', 'future'],
    packages=['pipcheck'],
    scripts=[],
    tests_require=['nose', 'coverage', 'unittest2', 'mock'],
    entry_points={
        'console_scripts': [
            'pipcheck = pipcheck.main:main',
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.4',
    ],
)
