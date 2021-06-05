"""
Implement an "AI" for a game of word guessing.

(We excluded Exercise 5, Problem 2 as too simple for the contracts. However,
the problem is re-introduced in this problem as well, so we merge the two problems in
one.

Additionally, we exclude the parts a) and b) from the original problem as they are
not really interesting for the contracts but are rather focused on teaching concepts
of inheritance. We therefore focus on part c) of the problem, which is much more complex
and algorithmically more involving.)

The computer picks randomly a word ``w`` from a pre-defined list of words. In each round
of the game, the player needs to guess a word. Based on the guess ``g``, the computer
returns one or more possible hints:

* ``w`` starts with ``g``.
* ``w`` ends with ``g``.
* ``w`` contains ``g``.
* ``w`` does not contain ``g``.

The game ends when the player hits the word.

The "AI" guesses the word automatically (given the pre-defined list of words). How many
rounds on average does it take the artificial player to finish the game?

"""
