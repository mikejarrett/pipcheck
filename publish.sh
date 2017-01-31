#! /bin/bash

show_help () {
	echo "Simple publishing script for Python projects"
	echo
	echo "usage: ./publish.sh [-h] [-v=VERSION] [-p]"
	echo "optional arguments:"
	echo "-h, --help   		Show this help message and exit"
	echo "-v, --version		Update to version and commit"
	echo "-p, --publish		If CI passes, publish to PyPI."
}

bumpversion_and_commit() {
	sed -ri "s/(__version__ = ')(.*)'/\1$VERSION'/g" pipcheck/__init__.py
    git add pipcheck/__init__.py
    git commit -m "Bump version to $VERSION"

	git ls-files --other --error-unmatch . >/dev/null 2>&1; ec=$?
	if [ "$ec" = 0 ] ; then
		echo "There are some untracked files. Not publishing."
        exit 1
	elif [ "$ec" = 1 ]; then
		echo "No untracked files"
	else
		echo "Received an error from ls-files"
		exit 1
	fi
}

export PUBLISH=0
export VERSION=

while true ; do
  case "$1" in
    -h) show_help ; exit 0 ;;
	-v|--version) export VERSION="$2" ; shift 2 ;;
    -p|--publish) export PUBLISH="1" ; shift 1 ;;
    *) break ;;
  esac
done

echo "Bumping to version $VERSION"
echo "Publishing $PUBLISH"

echo "Running tests..."
if tox ; then
    echo ''
else
    exit 1
fi

echo "Running Pylint..."
pylint --rcfile=.pylintrc pipcheck > pylint.txt
if [ $? -ne 0 ] ; then
    echo "Pylint exited unexpectedly. Stopping the build process."
    exit 1

elif [ -s pylint.txt ] ; then
    echo "Pylint violations. Stopping the build process."
    exit 1

else
    rm -f pylint.txt
fi

echo "Checking Python code style..."
pycodestyle --config=.pycodestylerc pipcheck > pycodestyle.txt
if [ $? -ne 0 ] ; then
    echo "Pycodestyle exited unexpectedly. Stopping the build process."
    exit 1

elif [ -s pycodestyle.txt ] 
then
    echo "Code style violations. Stopping build process."
    exit 1

else
    rm -f pycodestyle.txt
fi

if [ ! -z "$VERSION" ] ; then
	bumpversion_and_commit
fi

if [ "$PUBLISH" = "1" ] ; then
    python setup.py sdist upload -r pypi

    if [ $? -eq 0 ] ; then
        echo "All done!"

    else
        echo "Error from sdist upload"
    fi
fi
