# aocdbc

.. image:: https://github.com/mristin/aocdbc/actions/workflows/test-on-push-to-main.yml/badge.svg
    :target: https://github.com/mristin/aocdbc/actions/workflows/test-on-push-to-main.yml
    :alt: Test on push to main

.. image:: https://coveralls.io/repos/github/mristin/aocdbc/badge.svg?branch=main
    :target: https://coveralls.io/github/mristin/aocdbc?branch=main

We present here the solutions for the exercises of the `Advent of Code 2020`_ written
in Python and annotated with `contracts`_.
This provides a data set of 25 programs with contracts specified using
`icontract`_ to support the development of tools for automated testing such as
`crosshair`_ and `icontract-hypothesis`_.

.. _Advent of Code 2020: https://adventofcode.com/2020
.. _contracts: https://en.wikipedia.org/wiki/Design_by_contract
.. _icontract: https://github.com/mristin/icontract
.. _crosshair: https://github.com/pschanely/CrossHair
.. _icontract-hypothesis: https://github.com/mristin/icontract-hypothesis

The design-by-contract is still not widely practiced in Python due to different factors
such as unfamiliarity of the community with the concept and with the available tools.
Therefore we could not find a sufficiently large and representative code base that
would give us a good testbed for the automatic tools.

Hence we employ the programming puzzles of the `Advent of Code 2020`_ as a
**benchmark** to compare and evaluate different approaches to automatic testing of
Python code.

We expect this data set to help us **discover the blind spots**.
The tools (usually) generate the input for the functions based on the type annotations
and pre-conditions.
Which families of pre-conditions are supported?
What are the limits of a testing tool and which pre-conditions are not supported?
Which kinds of inputs can be generated in a computationally efficient way?

We hope that this code base benefits not only the community of **tool developers** but
also the **tool users**.
The data set should make apparent the involved **trade-offs**.
In particular, the users should learn based on practical examples how the tools differ,
understand their limits and distinguish in which cases a tool is better than
the others.

Contributing
============
If you would like to submit your solution with different contracts to one or
more exercises, please `create a pull request`_.

You can also just `create an issue`_ and post a code snippet, if that is easier for you.

.. _create a pull request: https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork
.. _create an issue: https://github.com/mristin/aocdbc/issues/new
