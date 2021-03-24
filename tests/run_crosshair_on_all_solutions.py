import pathlib
import subprocess
import os
import sys


def main() -> None:
    tests_dir = pathlib.Path(os.path.realpath(__file__)).parent
    aocdbc_dir = tests_dir.parent / "aocdbc"

    for i, pth in enumerate(sorted(aocdbc_dir.glob("day_*.py"))):
        if i > 0:
            print()

        print(f"Running crosshair on: {pth}")
        subprocess.check_call([sys.executable, '-m', 'crosshair', 'check', str(pth)])


if __name__ == "__main__":
    main()
