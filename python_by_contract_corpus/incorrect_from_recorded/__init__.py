# pylint: disable=all

"""
Provide programs as solutions to problems with bugs.

These programs are based on the recorded failures that we eventually re-introduced in
the (apparently correct) final solutions.

We could not reproduce the following failure cases since they were either not
informative enough or the final and the recorded solution diverged too much:

* archived/recorded_failures/aoc2020/day_3_toboggan_trajectory/empty_line_at_end_when_split_on_newline.py
* archived/recorded_failures/aoc2020/day_7_handy_haversacks/dont_count_outer_bag.py
* archived/recorded_failures/aoc2020/day_9_encoding_error/postcondition_cannot_handle_nonetype.py
* archived/recorded_failures/aoc2020/day_11_seating_system/invalid_state_change_caught_by_contracts.py
* archived/recorded_failures/aoc2020/day_12_rain_risk/invalid_orientation.py
* archived/recorded_failures/aoc2020/day_12_rain_risk/regex_incorrectly_ended.py
* archived/recorded_failures/aoc2020/day_18_operation_order/empty_expressions.py
* archived/recorded_failures/aoc2020/day_18_operation_order/empty_tails.py
* archived/recorded_failures/aoc2020/day_18_operation_order/negative_numbers.py
* archived/recorded_failures/aoc2020/day_22_crab_combat/play_a_round_failed_on_edge_case.py
* archived/recorded_failures/aoc2020/day_22_crab_combat/play_a_round_failed_on_another_edge_case.py
* archived/recorded_failures/aoc2020/day_25_combo_breaker/forgot_to_return.py
* archived/recorded_failures/ethz_eprog_2019/exercise_04/problem_02/missed_edge_case.py
* archived/recorded_failures/ethz_eprog_2019/exercise_06/problem_04/forgot_an_edge_case_when_checking_same_order_on_empty_list.py
* archived/recorded_failures/ethz_eprog_2019/exercise_06/problem_04/forgot_to_sync_first_and_last.py
* archived/recorded_failures/ethz_eprog_2019/exercise_06/problem_04/got_add_last_wrong.py
* archived/recorded_failures/ethz_eprog_2019/exercise_07/problem_02/got_split_wrong.py
* archived/recorded_failures/ethz_eprog_2019/exercise_08/problem_03/got_leaving_customer_wrong.py
* archived/recorded_failures/ethz_eprog_2019/exercise_11/problem_01/missed_edge_case_in_postcondition_where_all_grades_are_zero.py
* archived/recorded_failures/ethz_eprog_2019/exercise_11/problem_02/got_startpos_endpos_wrong_in_tokenization.py
* archived/recorded_failures/ethz_eprog_2019/exercise_11/problem_02/missing_edge_cases_for_evaluation.py

Additionally, we excluded the following failures since they were underspecified in
the exercise description:

* archived/recorded_failures/ethz_eprog_2019/exercise_12/problem_03/forgot_to_specify_what_happens_if_the_result_is_too_large.py
* archived/recorded_failures/ethz_eprog_2019/exercise_12/problem_03/forgot_to_specify_what_happens_on_math_errors_in_function_call.py
"""
