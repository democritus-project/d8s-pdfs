#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort democritus_pdfs/ tests/

black democritus_pdfs/ tests/

mypy democritus_pdfs/ tests/

pylint --fail-under 9 democritus_pdfs/*.py

flake8 democritus_pdfs/ tests/

bandit -r democritus_pdfs/

# we run black again at the end to undo any odd changes made by any of the linters above
black democritus_pdfs/ tests/
