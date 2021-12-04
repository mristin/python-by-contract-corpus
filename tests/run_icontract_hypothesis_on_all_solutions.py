"""Run icontract-hypothesis on all solutions without obvious bugs."""

import pathlib
import subprocess
import os
import sys


def main() -> None:
    tests_dir = pathlib.Path(os.path.realpath(__file__)).parent
    src_dir = tests_dir.parent / "python_by_contract_corpus/correct"

    for i, pth in enumerate(sorted(src_dir.glob("**/*.py"))):
        if i > 0:
            print()

        print(f"Running icontract-hypothesis on: {pth}")
        subprocess.check_call(
            [sys.executable, "-m", "icontract_hypothesis", "test", "--path", str(pth)]
        )


if __name__ == "__main__":
    main()
