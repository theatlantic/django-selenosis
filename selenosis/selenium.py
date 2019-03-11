from __future__ import unicode_literals, absolute_import

import os
import sys
import unittest
from unittest import SkipTest

from django.test import LiveServerTestCase
import six
from django.utils.module_loading import import_string
from django.utils.text import capfirst


class SelenosisTestCaseBase(type(LiveServerTestCase)):
    # List of browsers to dynamically create test classes for.
    browsers = []
    # Sentinel value to differentiate browser-specific instances.
    browser = None

    def __new__(cls, name, bases, attrs):
        """
        Dynamically create new classes and add them to the test module when
        multiple browsers specs are provided (e.g. --selenium=firefox,chrome).
        """
        test_class = super(SelenosisTestCaseBase, cls).__new__(cls, name, bases, attrs)
        # If the test class is either browser-specific or a test base, return it.
        is_test_attr = lambda n: n.startswith('test') and callable(getattr(test_class, n))
        if test_class.browser or not any(is_test_attr(name) for name in dir(test_class)):
            return test_class
        elif test_class.browsers:
            # Reuse the created test class to make it browser-specific.
            # We can't rename it to include the browser name or create a
            # subclass like we do with the remaining browsers as it would
            # either duplicate tests or prevent pickling of its instances.
            first_browser = test_class.browsers[0]
            test_class.browser = first_browser
            # Create subclasses for each of the remaining browsers and expose
            # them through the test's module namespace.
            module = sys.modules[test_class.__module__]
            for browser in test_class.browsers[1:]:
                browser_test_class = cls.__new__(
                    cls,
                    str("%s%s" % (capfirst(browser), name)),
                    (test_class,),
                    {'browser': browser, '__module__': test_class.__module__}
                )
                setattr(module, browser_test_class.__name__, browser_test_class)
            return test_class
        # If no browsers were specified, skip this class (it'll still be discovered).
        return unittest.skip('No browsers specified.')(test_class)

    @classmethod
    def import_webdriver(cls, browser):
        if "." in browser:
            browser_import = browser
        elif browser.lower() in ('none', 'skip'):
            return
        else:
            browser_import = "selenium.webdriver.%s.webdriver.WebDriver" % browser
        return import_string(browser_import)

    def create_webdriver(self, *args, **kwargs):
        import selenium
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        selenium_version = tuple(map(int, selenium.__version__.split('.')))

        browser, _, url = self.browser.partition('+')
        if url:
            kwargs.update({
                'desired_capabilities': getattr(DesiredCapabilities, browser.upper()),
                'command_executor': url,
            })
            browser = 'remote'
        elif browser == 'chrome-headless':
            from selenium.webdriver import ChromeOptions

            browser = 'chrome'
            options = ChromeOptions()
            options.add_argument('headless')
            options.add_argument('disable-gui')
            options.add_argument('no-sandbox')
            if os.environ.get('CHROME_BIN'):
                options.binary_location = os.environ['CHROME_BIN']
            if selenium_version < (3, 8, 0):
                kwargs['chrome_options'] = options
            else:
                kwargs['options'] = options
        webdriver_cls = self.import_webdriver(browser)
        if webdriver_cls:
            return webdriver_cls(*args, **kwargs)


class SelenosisTestCase(six.with_metaclass(SelenosisTestCaseBase, LiveServerTestCase)):

    skip_selenium_exception = False

    @classmethod
    def setUpClass(cls):
        try:
            selenium = cls.create_webdriver()
        except Exception as e:
            if not cls.skip_selenium_exception:
                raise
            exc = SkipTest("%s" % e)
            six.reraise(SkipTest, exc, sys.exc_info()[2])
        if not selenium:
            if cls.skip_selenium_exception:
                raise SkipTest("Selenium configured incorrectly")
            else:
                raise Exception("Selenium configured incorrectly")
        cls.selenium = selenium
        cls.selenium.implicitly_wait(10)
        super(SelenosisTestCase, cls).setUpClass()

    @classmethod
    def _tearDownClassInternal(cls):
        # quit() the WebDriver before attempting to terminate and join the
        # single-threaded LiveServerThread to avoid a dead lock if the browser
        # kept a connection alive.
        if hasattr(cls, 'selenium'):
            cls.selenium.quit()
        super(SelenosisTestCase, cls)._tearDownClassInternal()
