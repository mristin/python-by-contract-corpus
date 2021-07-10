#!/usr/bin/env python3

"""Check that the distribution and python_by_contract_corpus/__init__.py are in sync."""
import subprocess
import sys
from typing import Optional, Dict

import python_by_contract_corpus


def main() -> int:
    """Execute the main routine."""
    success = True

    ##
    # Check basic fields
    ##

    setup_py = dict()  # type: Dict[str, str]

    fields = ["version", "author", "license", "description"]
    for field in fields:
        out = subprocess.check_output(
            [sys.executable, "setup.py", f"--{field}"], encoding="utf-8"
        ).strip()

        setup_py[field] = out

    if setup_py["version"] != python_by_contract_corpus.__version__:
        print(
            f"The version in the setup.py is {setup_py['version']}, "
            f"while the version in python_by_contract_corpus/__init__.py is: "
            f"{python_by_contract_corpus.__version__}",
            file=sys.stderr,
        )
        success = False

    if setup_py["author"] != python_by_contract_corpus.__author__:
        print(
            f"The author in the setup.py is {setup_py['author']}, "
            f"while the author in python_by_contract_corpus/__init__.py is: "
            f"{python_by_contract_corpus.__author__}",
            file=sys.stderr,
        )
        success = False

    if setup_py["license"] != python_by_contract_corpus.__license__:
        print(
            f"The license in the setup.py is {setup_py['license']}, "
            f"while the license in python_by_contract_corpus/__init__.py is: "
            f"{python_by_contract_corpus.__license__}",
            file=sys.stderr,
        )
        success = False

    if setup_py["description"] != python_by_contract_corpus.__doc__:
        print(
            f"The description in the setup.py is {setup_py['description']}, "
            f"while the description in python_by_contract_corpus/__init__.py is: "
            f"{python_by_contract_corpus.__doc__}",
            file=sys.stderr,
        )
        success = False

    ##
    # Classifiers need special attention as there are multiple.
    ##

    # This is the map from the distribution to expected status in __init__.py.
    status_map = {
        "Development Status :: 1 - Planning": "Planning",
        "Development Status :: 2 - Pre-Alpha": "Pre-Alpha",
        "Development Status :: 3 - Alpha": "Alpha",
        "Development Status :: 4 - Beta": "Beta",
        "Development Status :: 5 - Production/Stable": "Production/Stable",
        "Development Status :: 6 - Mature": "Mature",
        "Development Status :: 7 - Inactive": "Inactive",
    }

    classifiers = (
        subprocess.check_output(
            [sys.executable, "setup.py", f"--classifiers"], encoding="utf-8"
        )
        .strip()
        .splitlines()
    )

    status_classifier = None  # type: Optional[str]
    for classifier in classifiers:
        if classifier in status_map:
            status_classifier = classifier
            break

    if status_classifier is None:
        print(
            f"Expected a status classifier in setup.py "
            f"(e.g., 'Development Status :: 3 - Alpha'), but found none.",
            file=sys.stderr,
        )
        success = False
    else:
        expected_status_in_init = status_map[status_classifier]

        if expected_status_in_init != python_by_contract_corpus.__status__:
            print(
                f"Expected status {expected_status_in_init} "
                f"according to setup.py in python_by_contract_corpus/__init__.py, "
                f"but found: {python_by_contract_corpus.__status__}"
            )
            success = False

    if not success:
        return -1

    return 0


if __name__ == "__main__":
    sys.exit(main())
