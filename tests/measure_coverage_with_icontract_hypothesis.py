"""Run all the icontract-hypothesis specific tests and measure the code coverage."""

import argparse
import os
import pathlib
import subprocess
import sys


def main() -> int:
    """Execute the main routine."""
    this_path = pathlib.Path(os.path.realpath(__file__))
    subprocess.check_call(
        [
            "coverage",
            "run",
            "--source",
            "python_by_contract_corpus.correct",
            "-m",
            "tests.run_only_tests_with_icontract_hypothesis",
        ],
        cwd=str(this_path.parent),
    )
    subprocess.check_call(["coverage", "report"], cwd=str(this_path.parent))

    return 0


if __name__ == "__main__":
    sys.exit(main())
