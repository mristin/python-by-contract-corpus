# pylint: disable=all

"""
Provide programs as solutions to problems with bugs.

These programs are based on the recorded failures while we were solving the problems.
Whenever we encountered a bug, we recorded the state of the program. To make
the problems more focused, we took the solutions without obvious bugs
(see :mod:`python_by_contract_corpus.correct`) and manually introduced the recorded
bugs.

If we could not manually reproduce the bug by changing the correct solution,
the recorded failure was ignored. This was either because the recorded case was not
informative enough or because the recorded case was too far away from the final solution
to re-introduce the bug in a meaningful manner.

The initial and the final solutions oftentimes diverged as we had to completely change
the approach and re-model the problem with different abstractions to solve it.
Thus capturing a bug helped us in re-modelling, but it was later impossible to
re-trace the bug and re-introduce it since *knowing* about the bug changed the solution
in such a way to avoid it (*e.g.*, by using a different class hierarchy or different
responsibility domains of the functions).

Thus we excluded the following failure cases which we could not reproduce:

* recorded_failures/aoc2020/day_3_toboggan_trajectory/empty_line_at_end_when_split_on_newline.py
* recorded_failures/aoc2020/day_7_handy_haversacks/dont_count_outer_bag.py
* recorded_failures/aoc2020/day_9_encoding_error/postcondition_cannot_handle_nonetype.py
* recorded_failures/aoc2020/day_11_seating_system/invalid_state_change_caught_by_contracts.py
* recorded_failures/aoc2020/day_12_rain_risk/invalid_orientation.py
* recorded_failures/aoc2020/day_12_rain_risk/regex_incorrectly_ended.py
* recorded_failures/aoc2020/day_18_operation_order/empty_expressions.py
* recorded_failures/aoc2020/day_18_operation_order/empty_tails.py
* recorded_failures/aoc2020/day_18_operation_order/negative_numbers.py
* recorded_failures/aoc2020/day_22_crab_combat/play_a_round_failed_on_edge_case.py
* recorded_failures/aoc2020/day_22_crab_combat/play_a_round_failed_on_another_edge_case.py
* recorded_failures/aoc2020/day_25_combo_breaker/forgot_to_return.py
* recorded_failures/ethz_eprog_2019/exercise_04/problem_02/missed_edge_case.py
* recorded_failures/ethz_eprog_2019/exercise_06/problem_04/forgot_an_edge_case_when_checking_same_order_on_empty_list.py
* recorded_failures/ethz_eprog_2019/exercise_06/problem_04/forgot_to_sync_first_and_last.py
* recorded_failures/ethz_eprog_2019/exercise_06/problem_04/got_add_last_wrong.py
* recorded_failures/ethz_eprog_2019/exercise_07/problem_02/got_split_wrong.py
* recorded_failures/ethz_eprog_2019/exercise_08/problem_03/got_leaving_customer_wrong.py
* recorded_failures/ethz_eprog_2019/exercise_11/problem_01/missed_edge_case_in_postcondition_where_all_grades_are_zero.py
* recorded_failures/ethz_eprog_2019/exercise_11/problem_02/got_startpos_endpos_wrong_in_tokenization.py
* recorded_failures/ethz_eprog_2019/exercise_11/problem_02/missing_edge_cases_for_evaluation.py

Additionally, we excluded the following failures since they were underspecified in
the exercise description:

* recorded_failures/ethz_eprog_2019/exercise_12/problem_03/forgot_to_specify_what_happens_if_the_result_is_too_large.py
* recorded_failures/ethz_eprog_2019/exercise_12/problem_03/forgot_to_specify_what_happens_on_math_errors_in_function_call.py
"""
