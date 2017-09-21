#!/usr/bin/env python
import warnings
import selenosis


def main():
    warnings.simplefilter("error", Warning)
    runtests = selenosis.RunTests(
        "selenosis.tests.settings", "selenosis")
    runtests()


if __name__ == '__main__':
    main()
