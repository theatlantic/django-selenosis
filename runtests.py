#!/usr/bin/env python
import os
import warnings

import selenosis


def main():
    warnings.simplefilter("error", Warning)
    os.environ.setdefault('DJANGO_LIVE_TEST_SERVER_ADDRESS', 'localhost:8081-8089')
    runtests = selenosis.RunTests(
        "selenosis.tests.settings", "selenosis")
    runtests()


if __name__ == '__main__':
    main()
