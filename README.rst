*************************
Python-by-Contract Corpus
*************************

.. image:: https://github.com/mristin/python-by-contract-corpus/actions/workflows/test-on-push-to-main.yml/badge.svg
    :target: https://github.com/mristin/python-by-contract-corpus/actions/workflows/test-on-push-to-main.yml
    :alt: Test on push to main

.. image:: https://coveralls.io/repos/github/mristin/python-by-contract-corpus/badge.svg?branch=main
    :target: https://coveralls.io/github/mristin/python-by-contract-corpus?branch=main

We present here a corpus of Python programs annotated with `contracts`_.

The corpus includes:

* Solutions to the exercises of the `Advent of Code 2020`_, and
* Solutions to the exercises used during the lecture `"Introduction to Programming"`_ at ETH Zurich (Switzerland) in Fall 2019.

.. _contracts: https://en.wikipedia.org/wiki/Design_by_contract
.. _Advent of Code 2020: https://adventofcode.com/2020
.. _"Introduction to Programming": https://www.lst.inf.ethz.ch/education/archive/Fall2019/einfuehrung-in-die-programmierung-i--252-0027-.html
.. _icontract: https://github.com/mristin/icontract
.. _crosshair: https://github.com/pschanely/CrossHair
.. _icontract-hypothesis: https://github.com/mristin/icontract-hypothesis

The design-by-contract is still not widely practiced in Python due to different factors such as unfamiliarity of the community with the concept and with the available tools.
Therefore we could not find a sufficiently large and representative code base that would give us a good testbed for the automatic tools.

Hence we employ the solutions to the aforementioned exercises as a **benchmark** to compare and evaluate different approaches to automatic testing of Python code.

We expect this data set to help us **discover the blind spots**.
The tools (usually) generate the input for the functions based on the type annotations and pre-conditions.
So the corpus helps us answer the questions such as:

* Which families of pre-conditions are supported?
* What are the limits of a testing tool and which pre-conditions are not supported?
* Which kinds of inputs can be generated in a computationally efficient way?

We hope that this code base benefits not only the community of **tool developers** but also the **tool users** by exposing the involved **trade-offs**.
In particular, the users should learn based on practical examples how the tools differ, understand their limits and distinguish in which cases one tool is better than the other.

Contributing
============
If you would like to submit your solution with different contracts to one or more exercises, please `create a pull request`_.

You can also just `create an issue`_ and post a code snippet, if that is easier for you.

.. _create a pull request: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork
.. _create an issue: https://github.com/mristin/aocdbc/issues/new

Contributors
============
The solutions annotated with the contracts were provided by the following authors (equal contribution, in alphabetical order):

* `Lauren De bruyn <https://github.com/ProLoD>`_,
* `Marko Ristin <https://github.com/mristin>`_, and
* `Phillip Schanely <https://github.com/pschanely>`_.
