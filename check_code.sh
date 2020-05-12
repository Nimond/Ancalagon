#!/usr/bin/env bash
echo "Collecting python files..."
# TODO: check all python files
py_files=$(git ls-files -- '*.py' ':!:examples')

if ! poetry run isort -m 3 -tc --check-only ${py_files}; \
then
  echo "'isort' returned non-zero code"
  poetry run isort -m 3 -tc --diff ${py_files}
  exit 1
fi

if ! poetry run black -l 79 -S --check -q ${py_files}; \
then
  echo "'black' returned non-zero code"
  poetry run black -l 79 -S --diff -q ${py_files}
  exit 1
fi

echo ""
echo "Code:"
not_tests=$(git ls-files -- '*.py' ':!:examples' ':!:tests')
poetry run pylint ${not_tests} 
exit_code="$?"

if [ $(((exit_code & 1) >> 0)) -ne 0 ]; then
  echo "Fatal message issued by pylint"
  exit 1
elif [ $(((exit_code & 2) >> 0)) -ne 0 ]; then
  echo "Error message issued by pylint"
  exit 1
fi

echo ""
echo "Tests:"
tests=$(git ls-files -- '*.py' ':!:examples' ':!:ancalagon')
poetry run pylint ${tests} --disable=W0621,W0212
exit_code="$?"

if [ $(((exit_code & 1) >> 0)) -ne 0 ]; then
  echo "Fatal message issued by pylint"
  exit 1
elif [ $(((exit_code & 2) >> 0)) -ne 0 ]; then
  echo "Error message issued by pylint"
  exit 1
fi

echo "Nice."
