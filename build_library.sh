#!/bin/bash
python3 -m pip install --user --upgrade setuptools wheel twine

rm -r build dist
python3 setup.py sdist bdist_wheel
