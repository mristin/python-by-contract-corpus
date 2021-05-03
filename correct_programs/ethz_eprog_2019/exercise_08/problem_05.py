"""
Simulate the wolf fleeing a city.

A city is given as a grid of ``n x n`` crossroads. At each crossroad, the wolf picks
a random direction. The grid size ``n`` is greater than 1 and odd.

The wolf starts at ``(0, 0)``. The wolf escaped the city when he reaches the border
of the grid.

The wolf can never visit the same crossroad twice. If there are no more options,
the wolf is shot by the hunters and dies.

Estimate the probability of the wolf escaping the city.

(We deliberately exclude the parts of the exercise concerning the drawing of the paths
in the GUI.)
"""
