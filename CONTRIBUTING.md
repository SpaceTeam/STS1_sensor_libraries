
# Contributing to the Package

## Making a new release

* (On Raspberry Pi) Run `pytest`.
* Go to pyproject.toml and increase the version number.
* Go to docs/source/conf.py and increase the version number.
* Merge into main.
* Merge into release. This will automatically update the docs.
* On Github: Make a release. This will automatically publish it to PyPI.
