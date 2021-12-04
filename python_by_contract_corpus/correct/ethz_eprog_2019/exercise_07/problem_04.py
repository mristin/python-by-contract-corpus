"""
Write a program to draw a tree recursively.

Each branch forks in two, one sub-branch that goes clockwise and the other that goes
counter-clockwise. The tree is drawn in multiple steps. Each step is defined by a tuple
``(x, y, alpha, l)``:

* Starting point of the actual segment ``(x, y)``,
* The direction of the segment ``alpha``,
* The length of the segment ``l``.

The recursion stops when ``l < 10`` and ends with a leaf.

The forking of a branch occurs as follows. The sub-branch that goes clockwise follows
with ``l' = 0.8 * l`` and ``alpha' = alpha + PI / 5``. The sub-branch that goes
counter-clockwise follows with ``l'' = 0.6 * l`` and ``alpha'' = alpha  - PI / 3``.

The starting point of the sub-branches is the end point of the preceding segment.

Start the program with ``x = SIZE / 2, y = SIZE``, ``l_0 = 100`` and
``alpha_0 = PI / 2``, where ``SIZE`` is the size of the drawing canvas.
"""
