#!/bin/bash
python3 -m pip install --user --upgrade twine
twine upload dist/*
