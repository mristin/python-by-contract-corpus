#!/usr/bin/env python3
"""Run pre-commit checks on the repository."""
import argparse
import enum
import os
import pathlib
import subprocess
import sys


class Step(enum.Enum):
    BLACK = "black"
    MYPY = "mypy"
    TEST = "test"
    DOCTEST = "doctest"


def main() -> int:
    """"Execute entry_point routine."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--overwrite",
        help="Try to automatically fix the offending files (e.g., by re-formatting).",
        action="store_true",
    )
    parser.add_argument(
        "--select",
        help=(
            "If set, only the selected steps are executed. "
            "This is practical if some of the steps failed and you want to "
            "fix them in isolation. "
            "The steps are given as a space-separated list of: "
            + " ".join(value.value for value in Step)
        ),
        metavar="",
        nargs="+",
        choices=[value.value for value in Step],
    )
    parser.add_argument(
        "--skip",
        help=(
            "If set, skips the specified steps. "
            "This is practical if some of the steps passed and "
            "you want to fix the remainder in isolation. "
            "The steps are given as a space-separated list of: "
            + " ".join(value.value for value in Step)
        ),
        metavar="",
        nargs="+",
        choices=[value.value for value in Step],
    )

    args = parser.parse_args()

    overwrite = bool(args.overwrite)

    selects = (
        [Step(value) for value in args.select]
        if args.select is not None
        else [value for value in Step]
    )
    skips = [Step(value) for value in args.skip] if args.skip is not None else []

    repo_root = pathlib.Path(__file__).parent

    if Step.BLACK in selects and Step.BLACK not in skips:
        print("Black'ing...")
        # fmt: off
        black_targets = [
            "aocdbc",
            "tests",
            "precommit.py"
        ]
        # fmt: on

        if overwrite:
            subprocess.check_call(["black"] + black_targets, cwd=str(repo_root))
        else:
            subprocess.check_call(
                ["black", "--check"] + black_targets, cwd=str(repo_root)
            )
    else:
        print("Skipped black'ing.")

    if Step.MYPY in selects and Step.MYPY not in skips:
        print("Mypy'ing...")
        # fmt: off
        mypy_targets = ["aocdbc", "tests"]
        subprocess.check_call(["mypy", "--strict"] + mypy_targets, cwd=str(repo_root))
        # fmt: on
    else:
        print("Skipped mypy'ing.")

    if Step.TEST in selects and Step.TEST not in skips:
        print("Testing...")
        env = os.environ.copy()
        env["ICONTRACT_SLOW"] = "true"

        # fmt: off
        subprocess.check_call(
            [
                "coverage", "run",
                "--source", "aocdbc",
                "-m", "unittest", "discover"
            ],
            cwd=str(repo_root),
            env=env,
        )
        # fmt: on

        subprocess.check_call(["coverage", "report"])
    else:
        print("Skipped testing.")

    if Step.DOCTEST in selects and Step.DOCTEST not in skips:
        print("Doctesting...")
        subprocess.check_call([sys.executable, "-m", "doctest", "README.rst"])

        aocdbc_dir = repo_root / "aocdbc"
        for pth in sorted(aocdbc_dir.glob("**/*.py")):
            subprocess.check_call([sys.executable, "-m", "doctest", str(pth)])

    else:
        print("Skipped doctesting.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
