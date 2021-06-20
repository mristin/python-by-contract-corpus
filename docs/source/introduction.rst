************
Introduction
************

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
