*****************
Recorded Failures
*****************

As we developed the solutions to the exercises, we recorded failures detected by the our tools.
These records provide a material for education, further research and initial insights what bugs could be (easily) detected.

The recorded failures can be found at: https://github.com/mristin/python-by-contract-corpus/tree/main/recorded_failures

Important Notes
===============
Form
----
For the time being, the recorded failures consist of the source codes *at the time* of the failure.
This is not really optimal as it is hard to compare the working version of the recorded buggy source code with the final solution.
In the future, we want to re-phrase the buggy code by introducing the bug into the final solution.
The re-phrasing should allow the reader to easily differentiate the buggy from the final solution.

Bias
----
The mistakes that practically occur during the development are highly biased towards the skill level of the developer as well as his/her familiarity with the testing tools.
Since we were very few contributors, and the distribution of problem assignment was skewed towards two contributors rather than random, the current corpus is inevitably highly biased towards the dominant contributors.

Nevertheless, we still think that at least the initial practical insights can be won from the recorded failures despite this bias.