#!/bin/bash
sudo rm -r dist build
pip install -U setuptools wheel
echo Esegui questo\: python setup.py sdist bdist_wheel
