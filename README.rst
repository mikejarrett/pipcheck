pipcheck
========

pipcheck is an application that checks for updates for PIP packages that are
installed

Requirements
============

Required
--------

``python`` and the following modules

  - ``pip``

Optional
--------

 - ``nose`` for running tests
 - ``mock`` for running tests

Installation
============

Installation using pip:

.. code:: sh

    $ sudo pip install pipcheck

Installation from source:

.. code:: sh

    $ git clone https://github.com/mikejarrett/pipcheck.git
    $ cd pipcheck
    $ sudo python setup.py install

Usage
======

Python

.. code:: python

    >>> from pipcheck.pipcheck import Checker
    >>> checker = Checker(csv_file='/tmp/updates.csv', new_config='/tmp/updates.pip')
    >>> checker(get_all_updates=True, verbose=True)
    Update Django (1.5.5 to 1.6.2)
    Update clonedigger (Unknown)
    Update ipdb (up to date)
    Update ipython (1.2.1 to 2.0.0)
    Update pylint (0.15.2 to 1.1.0)


Command-line

.. code:: sh

    usage: pipcheck [-h] [-c [/path/file]] [-r [/path/file]] [-v] [-a]
    [-p [http://pypi.python.org/pypi]]
    pipcheck is an application that checks for updates for PIP packages that are  installed
    optional arguments:
    -h, --help            show this help message and exit
    -c [/path/file], --csv [/path/file]
                          Define a location for csv output
    -r [/path/file], --requirements [/path/file]
                          Define location for new requirements file output
    -v, --verbose         Display the status of updates of packages
    -a, --all             Returns results for all installed packages
    -p [http://pypi.python.org/pypi], --pypi [http://pypi.python.org/pypi]
                          Change the pypi server from
                          http://pypi.python.org/pypi

Licence
=======
Apache v2 License

http://www.apache.org/licenses/