******************
Incorrect Programs
******************

The recorded incorrect programs (see :ref:`Recorded Failures`), are ill-suited for development of the correctness tools.
When developing and evaluating a correctness tool we need to clearly distinguish between expected and collateral bugs, and whether our correctness tool is actually buggy.
However, we recorded the failures "on-the-go" while solving the programming problems.
Thus the recorded code often blurs the actual cause of errors and diverges substantially from the final solution.
Analyzing and tracing errors in such code is expectedly tedious and error-prone.

To provide a better and more precise testbed we converted the recorded failures into minimal changes of final solutions.
We analyzed the recorded failures and tried to manually re-introduce the bug into the final solution.
That way the incorrect program is minimally different to the apparently correct solution which makes such incorrect code easier to reason about and gives succinct and reduced test cases.

While we could re-introduce the most of the failures, some cases were not suitable for re-introduction.
This was either because the recorded case was not informative enough or because the recorded case diverged too much from the final solution to be re-introduced in a meaningful manner.
For example, the initial and the final solutions oftentimes pursued different directions as we had to completely change the approach and re-model the problem with different abstractions.
Thus capturing a bug helped us during the development for re-modelling, but it was later impossible to re-trace the bug and re-introduce it since *knowing* about the bug changed the solution in such a way that it was avoided (*e.g.*, by using a different class hierarchy or different responsibility domains of the functions).

Additionally, for some exercises, the specification of the problem was not detailed enough, so what appears to be a bug is actually an under-specification.
We consequently ignored such failure cases though they represent valid bugs.

The code of the incorrect programs can be found at: https://github.com/mristin/python-by-contract-corpus/tree/main/python_by_contract_corpus/incorrect_from_recorded

The complete list of the recorded failure cases which were ignored can be found at: https://github.com/mristin/python-by-contract-corpus/tree/main/python_by_contract_corpus/incorrect_from_recorded/__init__.py
