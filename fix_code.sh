#!/usr/bin/env bash
echo "Collecting python files..."
py_files=$(git ls-files -- '*.py' ':!:*/docs/*.py')

echo "Running isort (autoformatter) in place..."
isort -m 3 -tc -q $py_files

echo "Running black (autoformatter) in place..."
black -l 79 -S -q $py_files

echo "Done."
