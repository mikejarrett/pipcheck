#! /bin/bash
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

python setup.py sdist upload -r pypi

if [ $? -eq 0 ] ; then
    echo "All done!"

else
    echo "Uh-oh! :( :( :("
fi
