"""
Analyze the grades of the students.

Here's an example of the data

.. code-block::

    111111004  5.0  5.0  6.0
    111111005  3.75 3.0  4.0
    111111006  4.5  2.25 4.0

Every line represents a grading of a student. It starts with her matriculation number,
followed by space-delimited grades (between 1.0 and 6.0, floats). The grades correspond
to lectures 1, 2 and 3, respectively.

Provide the function ``critical`` which accepts two arguments, ``bound1`` and
``bound2``. The function lists all the students which have "critical" grades.
A student should appear only once in the list.

A student is "critical" if the grade for the first lecture is smaller-equal ``bound1``
and the sum of the grades for the lecture 2 and 3 is smaller than ``bound2``.

On the above example, ``critical(4, 8)`` gives:

.. code-block::

    111111005

Provide the function ``top`` which lists the students with the best grades. The
parameter ``limit`` determines the number of the "top" students. If the number of
students is less than ``limit``, return the list of all the students.

A student should appear only once in the resulting list. The students are compared
based on the sum of the grades in all the three lectures. If the sum of grades is
equal for two students, the order in the list is undefined (*i.e.* does not matter).

On the above example, ``top(2)`` might return both the output:

.. code-block::

    111111004
    111111005

and:

.. code-block::

    111111004
    111111006

(Both outputs are valid.)

The parameter ``limit`` is always greater than 0. Both ``bound1`` and ``bound2`` are
expected in the range ``[0.0, 100.0]``.

"""
