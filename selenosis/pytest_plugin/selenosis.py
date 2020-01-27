from __future__ import absolute_import

import argparse
import os

from selenosis.selenium import SelenosisTestCaseBase


class SelenosisDriverAction(argparse.Action):
    """
    Validate the comma-separated list of requested browsers.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        browsers = values.split(',')
        for browser in browsers:
            if browser.lower() == 'chrome-headless':
                browser = 'chrome'
            browser = browser.partition('+')[0]
            if browser.lower() in ("skip", "none"):
                continue
            try:
                SelenosisTestCaseBase.import_webdriver(browser)
            except ImportError:
                raise argparse.ArgumentError(
                    self, "Selenosis browser specification '%s' is not valid." % browser)

        if not browsers:
            try:
                SelenosisTestCaseBase.import_webdriver('phantomjs')
            except:
                browsers = ['skip']
            else:
                browsers = ['phantomjs']

        SelenosisTestCaseBase.browsers = browsers

        setattr(namespace, self.dest, browsers)


def pytest_addoption(parser):
    parser.addini(
        "chrome_bin",
        help="Path to the chrome binary",
        default=os.getenv('CHROME_BIN'))

    group = parser.getgroup("selenosis", "selenosis")
    group._addoption(
        "--selenosis-driver",
        action=SelenosisDriverAction,
        help="Selenium driver to use with django-selenosis",
        default="skip",
        metavar="str")
