#!/usr/bin/env python
import warnings
import django_admin_testutils


def main():
    warnings.simplefilter("error", Warning)
    runtests = django_admin_testutils.RunTests(
        "django_admin_testutils.tests.settings", "django_admin_testutils")
    runtests()


if __name__ == '__main__':
    main()
