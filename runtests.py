#!/usr/bin/env python
import os
import warnings

import selenosis


def main():
    warnings.simplefilter("error", Warning)

    warnings.filterwarnings(
        'once',
        message="'grappelli' defines default_app_config"
    )

    # Introduced in Python 3.7
    warnings.filterwarnings(
        'ignore',
        category=DeprecationWarning,
        message="Using or importing the ABCs from 'collections' instead of from 'collections.abc'",
    )

    runtests = selenosis.RunTests("tests.settings", "tests")
    runtests()


if __name__ == '__main__':
    main()
