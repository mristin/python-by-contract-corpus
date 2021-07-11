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
    PYLINT = "pylint"
    PYICONTRACT_LINT = "pyicontract-lint"
    TEST = "test"
    DOCTEST = "doctest"
    CHECK_INIT_AND_SETUP_COINCIDE = "check-init-and-setup-coincide"


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
            "python_by_contract_corpus",
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
        mypy_targets = ["python_by_contract_corpus", "tests"]
        subprocess.check_call(["mypy", "--strict"] + mypy_targets, cwd=str(repo_root))
        # fmt: on
    else:
        print("Skipped mypy'ing.")

    if Step.PYLINT in selects and Step.PYLINT not in skips:
        # fmt: off
        print("Pylint'ing...")
        pylint_targets = ["python_by_contract_corpus"]
        subprocess.check_call(
            ["pylint", "--rcfile=pylint.rc"] + pylint_targets, cwd=str(repo_root)
        )
        # fmt: on
    else:
        print("Skipped pylint'ing.")

    if Step.PYICONTRACT_LINT in selects and Step.PYICONTRACT_LINT not in skips:
        # fmt: off
        print("Pyicontract-lint'ing...")
        subprocess.check_call(
            ["pyicontract-lint", "python_by_contract_corpus", "tests"],
            cwd=str(repo_root)
        )
        # fmt: on
    else:
        print("Skipped pyicontract-lint'ing.")

    if Step.TEST in selects and Step.TEST not in skips:
        print("Testing...")
        env = os.environ.copy()
        env["ICONTRACT_SLOW"] = "true"

        # fmt: off
        subprocess.check_call(
            [
                "coverage", "run",
                "--source", "python_by_contract_corpus",
                "-m", "unittest", "discover", "--failfast"
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

        src_dir = repo_root / "python_by_contract_corpus"
        for pth in sorted(src_dir.glob("**/*.py")):
            subprocess.check_call([sys.executable, "-m", "doctest", str(pth)])

    else:
        print("Skipped doctesting.")

    if (
        Step.CHECK_INIT_AND_SETUP_COINCIDE in selects
        and Step.CHECK_INIT_AND_SETUP_COINCIDE not in skips
    ):
        print(
            "Checking that python_by_contract_corpus/__init__.py and "
            "setup.py coincide..."
        )
        subprocess.check_call([sys.executable, "check_init_and_setup_coincide.py"])
    else:
        print(
            "Skipped checking that python_by_contract_corpus/__init__.py and "
            "setup.py coincide."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
