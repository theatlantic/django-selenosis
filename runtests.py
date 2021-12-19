#!/usr/bin/env python
import os
import warnings

import selenosis


def main():
    warnings.simplefilter("error", Warning)

    # Introduced in Python 3.7
    warnings.filterwarnings(
        'ignore',
        category=DeprecationWarning,
        message="Using or importing the ABCs from 'collections' instead of from 'collections.abc'",
    )
    warnings.filterwarnings('ignore', "'grappelli' defines default_app_config")

    os.environ.setdefault('DJANGO_LIVE_TEST_SERVER_ADDRESS', 'localhost:8081-8089')
    runtests = selenosis.RunTests(
        "selenosis.tests.settings", "selenosis")
    runtests()


if __name__ == '__main__':
    main()
