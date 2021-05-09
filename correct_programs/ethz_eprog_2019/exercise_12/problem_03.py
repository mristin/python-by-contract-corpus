# pylint: disable=line-too-long
"""
Implement a compiler for the interpreter developed in Exercise 12, Problem 1.

The program should be compiled in a language based on operand stack.

The following operations are supported:
* ``CONST c``: push the value ``c`` on the stack,
* ``LOAD v``: load the value of the variable ``v`` and push it on the stack,
* ``STORE v``: pop a value from the stack and store it to the variable ``v``,
* ``OP {operation}``: pop two values ("left" and "right"), apply the operation and
  push the result on the stack, and
* ``FUNC f``: pop a value from the stack, apply the function ``f`` on it and push the
  result on the stack.

Please see `page 5`_ of the exercise for an example.

.. _page 5: https://ethz.ch/content/dam/ethz/special-interest/infk/inst-cs/lst-dam/documents/Education/Classes/Fall2019/0027_Intro/Homework/u12.pdf?page=5
"""
