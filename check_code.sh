#!/usr/bin/env bash
echo "Collecting python files..."
# TODO: check all python files
py_files=$(git ls-files -- '*.py' ':!:examples')

if ! isort -m 3 -tc --check-only ${py_files}; \
then
  echo "'isort' returned non-zero code"
  isort -m 3 -tc --diff ${py_files}
  exit 1
fi

if ! black -l 79 -S --check -q ${py_files}; \
then
  echo "'black' returned non-zero code"
  black -l 79 -S --diff -q ${py_files}
  exit 1
fi

pylint ${py_files}
exit_code="$?"

if [ $(((exit_code & 1) >> 0)) -ne 0 ]; then
  echo "Fatal message issued by pylint"
  exit 1
elif [ $(((exit_code & 2) >> 0)) -ne 0 ]; then
  echo "Error message issued by pylint"
  exit 1
fi

echo "Nice."
