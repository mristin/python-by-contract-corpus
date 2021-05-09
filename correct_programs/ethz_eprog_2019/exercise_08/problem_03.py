"""
Simulate a shopping queue in discrete steps.

Here are the inputs:

* Number of checkouts with the respective efficiency ``p_0, p_1, ..., p_n`` with
  ``0 <= p_i < 1``.
  In every step, the cashier ``i`` scans with a probability ``p_i`` an item from the
  shopping cart of the customer at the front of the queue. When all the items from
  the shopping cart have been scanned, the customer leaves the queue.
* A new customer enters the queues with a probability ``e, 0 <= e < 1`` at every step.
* The size of the shopping cart ``w``. Every customer has a random number of items
  between 0 and ``w``.
* Customers are lazy. Given a laziness factor ``f``, the customers change to a shorter
  queue as soon as it is ``f`` people shorter than the actual position in the queue.

Provide the following metrics of the simulation:
* ``finished``: Number of people who left the queue at the end of the simulation.
* ``avg_queue_lengths``: A list of the average length of each queue during
   the simulation
* ``max_queue_lengths``: A list of the maximum length of each queue during
  the simulation
"""
