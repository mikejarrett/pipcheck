pipcheck
========
pipcheck is an application that checks for updates for PIP packages that are
installed

Installation
============
Installation using pip:
    $ pip install pipcheck

Installation from source:
    $ git clone < repositry  >
    $ cd pipcheck
    $ sudo python setup.py install

Usage
======
```
>>> from pipcheck.pipcheck import Checker
>>> checker = Checker(csv_file='/tmp/updates.csv', new_config='/tmp/updates.pip')
>>> checker()
Update pylint (0.15.2 to 1.1.0)
Update Django (1.5.5 to 1.6.2)
Update ipython (1.2.1 to 2.0.0)
>>>
```


##Command-line
```
usage: pipcheck [-h] [-c [/path/file]] [-r [/path/file]]
                [-p [http://pypi.python.org/pypi]]

pipcheck is an application that checks for updates for PIP packages that are installed

optional arguments:
  -h, --help            show this help message and exit
  -c [/path/file], --csv [/path/file]
                        Define a location for csv output
  -r [/path/file], --requirements [/path/file]
                        Define location for new requirements file output
  -p [http://pypi.python.org/pypi], --pypi [http://pypi.python.org/pypi]
                        Change the pypi server from
                        http://pypi.python.org/pypi
```

Licence
=======
Apache v2 License

http://www.apache.org/licenses/
