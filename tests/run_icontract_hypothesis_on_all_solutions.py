import pathlib
import subprocess
import os
import sys


def main() -> None:
    tests_dir = pathlib.Path(os.path.realpath(__file__)).parent
    correct_programs_dir = tests_dir.parent / "correct_programs"

    for i, pth in enumerate(sorted(correct_programs_dir.glob("**/test_*.py"))):
        if i > 0:
            print()

        print(f"Running icontract-hypothesis on: {pth}")
        subprocess.check_call(
            [sys.executable, "-m", "icontract_hypothesis", "test", "--path", str(pth)]
        )


if __name__ == "__main__":
    main()
