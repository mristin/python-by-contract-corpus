***************************
Details about the Exercises
***************************

We picked only the subset of the exercises.
The original exercises encompassed broader topics than programming (such as Extended Backus–Naur form, or short EBNF), so we skipped them.
Additionally, we skipped the exercises such as the Exercise 0 which introduced the students to version control and usage of IDEs.
As the course was meant to teach Java, some exercises focused on Java-specific topics.
Since we are collecting a corpus of Python programs annotated with contracts, we skipped such exercises as we did not deem them relevant for the corpus.
Some of the exercises involve programming of the graphical user interfaces (GUIs).
While contracts are indeed very useful in the GUI programming, we consider GUI programming to be out-of-scope for the current corpus.
Finally, we excluded the problems which we thought were too simple such as dealing with basic input/output operations (such as Exercise 2, Problem 4).

The original problem statements are much longer and more elaborate.
As our focus is on the source code, we shortened the text as much as possible and give it here only as orientation about the complexity of the exercises.
The problems themselves were sometimes simplified to make for a more pointed and easier-to-read code (*e.g.*, Exercise 6, Problem 5).
We explicitly marked the corresponding changes in the description of the problem.

Please refer to the original text (in German) for more details about the exercises.

The original content of the exercises is courtesy of Laboratory for Software Technology, ETH Zurich, which also bears the copyright.
A special thanks goes to `Prof. Thomas Gross`_ for pointing us to the exercises and sharing them with the public!

.. _Prof. Thomas Gross: https://inf.ethz.ch/de/personen/people-atoz/person-detail.tgross.html

You can find the original exercises at:
https://www.lst.inf.ethz.ch/education/archive/Fall2019/einfuehrung-in-die-programmierung-i--252-0027-.html

Reasons for Exclusions
======================

We provide in the following the complete list of skipped problems and the reason for exclusion:

Exercise 0 and 1
----------------
Exercise 0 and Exercise 1 are introductory exercises about EBNF, how to use version control and IDE.

Exercise 2
----------
* Problem 1 introduces general debugging practices in IDE.
* Problem 4 teaches console I/O which is too simple for contracts.

Exercise 4
----------
* Problem 4 focuses on programming graphical user interfaces (GUIs) in Java.

Exercise 5
----------
* Problem 1 concerns unit testing with JUnit.
* Problem 2 is too simple for the contracts.
* Problem 5 is a GUI exercise.

Exercise 6
----------
* Problem 2 is Java-specific (introducing how to work with constructors and classes).
  In our opinion, it was an extension of Exercise 5, problem 3 which does not bring enough material in terms of contracts to merit the inclusion in the corpus.

* Problem 3 is about black-box testing with JUnit, hence no solution can be written in Python.
  However, it would be interesting in the future work to see how contracts can help black-box testing.

Exercise 7
----------
* Problem 1 is almost identical to Exercise 6, Problem 4.
  Namely, a double-linked list needs to be implemented instead of a single-linked list.
  Since the interfaces and the contracts are the same, the solution to this problem would bring about nothing new in terms of contracts, so we decided to exclude it.

* Problem 3 is about EBNF and not a programming exercise.

Exercise 8
----------
* Problem 4 concerns the black-box testing.

Exercise 9
----------
* Problem 1 teaches the class hierarchy in Java, so we exclude it as irrelevant for the contracts.
* Problem 5 asks for implementation of a game.
  It would be really interesting to see how contracts help game development, but this is out-of-scope for the current corpus.

.. _details-exclusion-exercise-10:

Exercise 10
-----------
* Problem 1 is focused on concepts of object-oriented programming such as interfaces and classes.
  The problem statements was very complex to motivate complex class hierarchies, but we found the solution to have a limited contribution in terms of contracts.
* Problem 2 is about drawing a map in the GUI.
  Similar to other GUI-related problems, we skip it and leave it for future work.
* Problem 3 makes the student practice exceptions, which is not relevant for our corpus.

Exercise 11
-----------
* Problem 3 explains how to draw functions in GUI.

* Problem 4 focuses on interfaces and their application.
  It would be a nice example for demonstrating inheritance of the contracts, but involves GUI programming, so we exclude it.

Exercise 12
-----------
* Problem 2 requires drawing the shapes on the screen. We exclude the problem as it is GUI-related.
* Problem 5 is not a programming problem (but concerns Hoare triples ;-)).
