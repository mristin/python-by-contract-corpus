"""
Simulate a shopping queue in discrete steps.

Here are the inputs:

* Number of checkouts with the respective efficiency ``p_0, p_1, ..., p_n`` with
  ``0 <= p_i < 1``.
  In every step, the cashier ``i`` scans with a probability ``p_i`` an item from the
  shopping cart of the customer at the front of the queue. When all the items from
  the shopping cart have been scanned, the customer leaves the queue.
* A new customer shows up with a probability ``e, 0 <= e < 1`` at every step and
  enters one of the queues at random.
* The size of the shopping cart ``w``. Every customer has a random number of items
  between 0 and ``w``.

(We removed the feature "laziness factor" from the original problem statement.
The feature was not very clear to us, and would not have had much impact
on the contracts.)

Provide the following metrics of the simulation:

* ``finished``: Number of people who left the queue at the end of the simulation.
* ``avg_queue_lengths``: A list of the average length of each queue during
  the simulation
* ``max_queue_lengths``: A list of the maximum length of each queue during
  the simulation
"""
import random
import statistics
from typing import List, cast

from icontract import require, ensure, DBC


class Probability(DBC, float):
    """Represent a probability value."""

    @require(lambda value: 0 <= value < 1)
    def __new__(cls, value: float) -> "Probability":
        """Enforce the properties of a probability on ``value``."""
        return cast(Probability, value)


class Specs(DBC):
    """Specify the parameters of the simulation."""

    # fmt: off
    @require(
        lambda max_cart_size:
        max_cart_size >= 1
    )
    @require(
        lambda checkout_efficiencies:
        len(checkout_efficiencies) > 0
    )
    # fmt: on
    def __init__(
        self,
        checkout_efficiencies: List[Probability],
        new_customer_probability: Probability,
        max_cart_size: int,
    ) -> None:
        """Initialize with the given values."""
        self.checkout_efficiencies = checkout_efficiencies
        self.new_customer_probability = new_customer_probability
        self.max_cart_size = max_cart_size

    def __repr__(self) -> str:
        """Represent the specs for easier debugging."""
        return (
            f"Specs(\n"
            f"    checkout_efficiencies={self.checkout_efficiencies!r},\n"
            f"    new_customer_probability={self.new_customer_probability!r},\n"
            f"    max_cart_size={self.max_cart_size!r}\n"
            f")"
        )


class Stats(DBC):
    """Structure the results of the simulation."""

    # fmt: off
    @require(lambda finished: finished >= 0)
    @require(
        lambda avg_queue_lengths:
        all(
            an_avg >= 0
            for an_avg in avg_queue_lengths
        )
    )
    @require(
        lambda max_queue_lengths:
        all(
            a_max >= 0
            for a_max in max_queue_lengths
        )
    )
    # fmt: on
    def __init__(
        self,
        finished: int,
        avg_queue_lengths: List[float],
        max_queue_lengths: List[float],
    ) -> None:
        """Initialize with the given values."""
        self.finished = finished
        self.avg_queue_lengths = avg_queue_lengths
        self.max_queue_lengths = max_queue_lengths


class Customer:
    """Represent the current state of the customer in the simulation."""

    @require(lambda items_in_cart: items_in_cart >= 0)
    def __init__(self, items_in_cart: int) -> None:
        """Initialize with the given values."""
        self.items_in_cart = items_in_cart


# fmt: off
@require(lambda steps: steps >= 1)
@ensure(
    lambda result:
    all(
        avg_queue_length <= max_queue_length
        for avg_queue_length, max_queue_length in zip(
            result.avg_queue_lengths, result.max_queue_lengths)
    )
)
@ensure(
    lambda specs, result:
    len(result.avg_queue_lengths) == len(specs.checkout_efficiencies)
)
@ensure(
    lambda specs, result:
    len(result.max_queue_lengths) == len(specs.checkout_efficiencies)
)
# fmt: on
def simulate(specs: Specs, steps: int) -> Stats:
    """Simulate in ``steps`` number of iterations according to the ``specs``."""
    finished = 0

    # Length of the queues at each step
    queues = [[] for _ in specs.checkout_efficiencies]  # type: List[List[Customer]]

    # The length of all the queues at each step
    queue_lengths = [[] for _ in specs.checkout_efficiencies]  # type: List[List[int]]

    for _ in range(steps):
        # Process an item
        for queue, efficiency in zip(queues, specs.checkout_efficiencies):
            if len(queue) > 0:
                customer = queue[0]
                assert customer.items_in_cart > 0

                if random.random() < efficiency:
                    customer.items_in_cart -= 1
                    if customer.items_in_cart == 0:
                        queue.pop(0)
                        finished += 1

        # Enter new customer
        if random.random() < specs.new_customer_probability:
            queue_index = random.randint(0, len(queues) - 1)
            queues[queue_index].append(
                # ERROR (mristin, 2021-06-03):
                # I got the range for the ``items_in_cart`` wrong.
                # It is a off-by-one error and should have been something like:
                # Customer(items_in_cart=random.randint(1, specs.max_cart_size))
                Customer(items_in_cart=random.randint(0, specs.max_cart_size))
            )

        # Compute stats for the step
        for queue, lengths in zip(queues, queue_lengths):
            lengths.append(len(queue))

    # fmt: off
    assert len(queue_lengths) == len(specs.checkout_efficiencies)
    assert all(
        len(entry) == steps
        for entry in queue_lengths
    ), f"{steps=}, {len(queue_lengths)=}, {[len(entry) for entry in queue_lengths]=}"
    # fmt: on

    return Stats(
        finished=finished,
        avg_queue_lengths=[statistics.mean(lengths) for lengths in queue_lengths],
        max_queue_lengths=[max(lengths) for lengths in queue_lengths],
    )
