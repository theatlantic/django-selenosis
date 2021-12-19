import argparse
import logging
import unittest

import django.test.runner

from selenosis.selenium import SelenosisTestCaseBase


class ActionSelenosis(argparse.Action):
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
        setattr(namespace, self.dest, browsers)


class NoFailFastUnexpectedSuccessTestResultMixin(object):
    """Overridden test result class that doesn't failfast on unexpected success"""

    def addUnexpectedSuccess(self, test):
        self.unexpectedSuccesses.append((test, 'Success'))
        if self.showAll:
            self.stream.writeln("unexpected success")
        elif self.dots:
            self.stream.write("u")
            self.stream.flush()

    def printErrors(self):
        super(NoFailFastUnexpectedSuccessTestResultMixin, self).printErrors()
        self.printErrorList('UNEXPECTED SUCCESS', self.unexpectedSuccesses)


class TextTestResult(NoFailFastUnexpectedSuccessTestResultMixin, unittest.TextTestResult):
    pass


class DebugSQLTextTestResult(
        NoFailFastUnexpectedSuccessTestResultMixin,
        django.test.runner.DebugSQLTextTestResult):

    def addUnexpectedSuccess(self, test):
        super(DebugSQLTextTestResult, self).addUnexpectedSuccess(test)
        self.debug_sql_stream.seek(0)
        self.unexpectedSuccesses[-1] += (self.debug_sql_stream.read(),)


class _FailedTest(unittest.TestCase):
    """
    Backported python 3.4+ test case for failures so that unittest failure
    exceptions are picklable

    See https://bugs.python.org/issue22903
    """
    _testMethodName = None

    def __init__(self, method_name, exception):
        self._exception = exception
        super(_FailedTest, self).__init__(method_name)

    def __getattr__(self, name):
        if name != self._testMethodName:
            return super(_FailedTest, self).__getattr__(name)

        def testFailure():
            raise self._exception

        return testFailure


class PatchedTestLoader(unittest.TestLoader):
    """
    Backported python 3.4+ test loader so that unittest failure exceptions are picklable

    See https://bugs.python.org/issue22903
    """

    def _find_tests(self, start_dir, pattern, **kwargs):
        super_iter = super(PatchedTestLoader, self)._find_tests(start_dir, pattern, **kwargs)
        for test_suite in super_iter:
            if len(test_suite._tests) == 1:
                test = test_suite._tests[0]
                if type(test).__name__ in ('ModuleImportFailure', 'LoadTestsFailure'):
                    suite_cls = type(test_suite)
                    method_name = test._testMethodName
                    # Trigger exception to find out its value
                    try:
                        getattr(test, method_name)()
                    except Exception as e:
                        test_suite = suite_cls((_FailedTest(method_name, e),))
            yield test_suite


class DiscoverRunner(django.test.runner.DiscoverRunner):
    """Overridden DiscoverRunner that doesn't failfast on unexpected success"""

    default_log_by_verbosity = False

    def __init__(self, **kwargs):
        self.log_by_verbosity = kwargs.pop('log_by_verbosity', False)
        browsers = kwargs.pop('selenium', None)
        if not browsers:
            try:
                SelenosisTestCaseBase.import_webdriver('chrome')
            except:
                browsers = ['skip']
            else:
                browsers = ['chrome-headless']
        SelenosisTestCaseBase.browsers = browsers

        if browsers == 'skip':
            self.exclude_tags.add('selenium')

        super(DiscoverRunner, self).__init__(**kwargs)

    def get_resultclass(self):
        return DebugSQLTextTestResult if self.debug_sql else TextTestResult

    @classmethod
    def add_arguments(cls, parser):
        super(DiscoverRunner, cls).add_arguments(parser)
        parser.add_argument(
            '--selenium', action=ActionSelenosis, metavar='BROWSERS',
            help='A comma-separated list of browsers to run the Selenosis '
                 'tests against. Defaults to "phantomjs".')
        parser.add_argument(
            '--%slog-by-verbosity' % ('no-' if cls.default_log_by_verbosity else ''),
            action=('store_false' if cls.default_log_by_verbosity else 'store_false'),
            default=cls.default_log_by_verbosity,
            dest='log_by_verbosity',
            help='%s matching log levels to the verbosity flag' % (
                'Disable' if cls.default_log_by_verbosity else 'Enable'))

    verbosity_log_levels = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }

    @property
    def log_level(self):
        return self.verbosity_log_levels[self.verbosity]

    def setup_test_environment(self, **kwargs):
        super(DiscoverRunner, self).setup_test_environment(**kwargs)
        from django.conf import settings
        if self.log_by_verbosity:
            loggers = settings.LOGGING.get('loggers') or {}
            for _, logger_opts in loggers.items():
                if 'level' not in logger_opts:
                    continue
                level = logging._checkLevel(logger_opts['level'])
                if level > self.log_level:
                    logger_opts['level'] = logging.getLevelName(self.log_level)
