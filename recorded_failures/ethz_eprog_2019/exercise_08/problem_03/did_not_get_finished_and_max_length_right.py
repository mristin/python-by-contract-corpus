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
import dataclasses
import random
import statistics
from typing import List

from icontract import require, ensure, DBC


class Specs(DBC):

    # fmt: off
    @require(
        lambda checkout_efficiencies:
        all(
            0 <= eff < 1
            for eff in checkout_efficiencies
        )
    )
    @require(
        lambda new_customer_probability:
        0 <= new_customer_probability < 1
    )
    @require(
        lambda max_cart_size:
        max_cart_size > 0
    )
    # fmt: on
    def __init__(
            self,
            checkout_efficiencies: List[float],
            new_customer_probability: float,
            max_cart_size: int) -> None:
        self.checkout_efficiencies = checkout_efficiencies
        self.new_customer_probability = new_customer_probability
        self.max_cart_size = max_cart_size

    def __repr__(self) -> str:
        return (
            f'Specs(\n'
            f'    checkout_efficiencies={self.checkout_efficiencies!r},\n'
            f'    new_customer_probability={self.new_customer_probability!r},\n'
            f'    max_cart_size={self.max_cart_size!r}\n'
            f')'
        )


class Stats(DBC):
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
            max_queue_lengths: List[float]) -> None:
        self.finished = finished
        self.avg_queue_lengths = avg_queue_lengths
        self.max_queue_lengths = max_queue_lengths


class Customer:
    @require(lambda items_in_cart: items_in_cart >= 0)
    def __init__(self, items_in_cart: int) -> None:
        self.items_in_cart = items_in_cart


# fmt: off
@require(lambda steps: steps >= 0)
@require(lambda specs: len(specs.checkout_efficiencies) > 0)
@ensure(
    lambda specs, result:
    len(result.avg_queue_lengths) == len(specs.checkout_efficiencies)
)
@ensure(
    lambda result:
    all(
        an_avg <= result.finished
        for an_avg in result.avg_queue_lengths
    )
)
@ensure(
    lambda specs, result:
    len(result.max_queue_lengths) == len(specs.checkout_efficiencies)
)
# ERROR:
# Falsifying example: execute(
#     kwargs={'specs': Specs(
#          checkout_efficiencies=[0.0],
#          new_customer_probability=0.42057158083084506,
#          max_cart_size=1
#      ), 'steps': 3},
# )
#
# icontract.errors.ViolationError:
# all(
#         a_max <= result.finished
#         for a_max in result.max_queue_lengths
#     ):
# all(
#         a_max <= result.finished
#         for a_max in result.max_queue_lengths
#     ) was False, e.g., with
#   a_max = 1
# result was <correct_programs.ethz_eprog_2019.exercise_08.problem_03.Stats object at 0x00000219D5092100>
# result.finished was 0
# result.max_queue_lengths was [1]
@ensure(
    lambda result:
    all(
        a_max <= result.finished
        for a_max in result.max_queue_lengths
    )
)
# fmt: on
def simulate(specs: Specs, steps: int) -> Stats:
    finished = 0

    # Length of the queues at each step
    queues = [[] for _ in specs.checkout_efficiencies]  # type: List[List[Customer]]

    # The length of all the queues at each step
    queue_lengths = [[] for _ in specs.checkout_efficiencies]  # type: List[List[int]]

    for _ in range(steps):
        # Process an item
        for i, (queue, efficiency) in enumerate(
                zip(queues, specs.checkout_efficiencies)):
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
        max_queue_lengths=[max(lengths) for lengths in queue_lengths]
    )
