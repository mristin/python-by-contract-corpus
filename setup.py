"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import os

from setuptools import setup, find_packages

# pylint: disable=redefined-builtin

here = os.path.abspath(os.path.dirname(__file__))  # pylint: disable=invalid-name

with open(os.path.join(here, "README.rst"), encoding="utf-8") as fid:
    long_description = fid.read()  # pylint: disable=invalid-name

with open(os.path.join(here, "requirements.txt"), encoding="utf-8") as fid:
    install_requires = [line for line in fid.read().splitlines() if line.strip()]

setup(
    name="python-by-contract-corpus",
    # Please don't forget to sync up with __init__.py!
    version="2021.7.10rc1",
    description=(
        "Provide a corpus of programs annotated with contracts "
        "with no obvious bugs."
    ),
    long_description=long_description,
    url="https://github.com/mristin/python-by-contract-corpus",
    author="Lauren De bruyn, Marko Ristin, Phillip Schanely",
    author_email="marko@ristin.ch",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    license="License :: OSI Approved :: MIT License",
    keywords="design-by-contract contracts automatic testing corpus",
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    # fmt: off
    extras_require={
        "dev": [
            "black==20.8b1",
            "mypy==0.812",
            "pylint==2.8.2",
            "pyicontract-lint>=2.1.3,<3"
            "coverage>=5.5,<6",
            "twine>=3.4.1,<4"
        ]
    },
    # fmt: on
    py_modules=["python_by_contract_corpus"],
    package_data={"python_by_contract_corpus": ["py.typed"]},
    data_files=[(".", ["LICENSE", "README.rst", "requirements.txt"])],
)
