# How to Contribute to Documentation

## How to Build

Change to the root directory of the repository.

Activate your virtual environment.

Install the requirements:

```
pip3 install -r requirements.txt
```

Install the documentation requirements:

```
pip3 install -r requirements-doc.txt
```

Build with Sphinx:

```
cd docs
sphinx-build source build
```

The documentation is in the `docs/build` directory.

## Style Guide

**Headings.**
Use the following heading style from [Sphinx tutorial][sphinx-sections]:

[sphinx-sections]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#sections

* `#` with overline, for parts
* `*` with overline, for chapters
* `=`, for sections
* `-`, for subsections
* `^`, for subsubsections
* `“`, for paragraphs

**Line length.**
Do not use line limit.

Put sentences on individual lines to make diff'ing easier.
