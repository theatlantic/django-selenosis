from io import StringIO
import logging
import unittest

import selenosis


logger = logging.getLogger(__name__)


class DiscoverRunnerTestCase(selenosis.SelenosisTestCase):

    class tag_decorator(selenosis.SelenosisTestCase):
        @selenosis.tag('tag1')
        def test_tag1(self):
            self.assertTrue(True)

        @selenosis.tag('tag2')
        def test_tag2(self):
            self.assertTrue(True)

    class unexpected_success_failfast(selenosis.SelenosisTestCase):
        @unittest.expectedFailure
        def test_a(self):
            self.assertTrue(True)

        def test_b(self):
            self.assertTrue(True)

    class log_by_verbosity(selenosis.SelenosisTestCase):
        def test_debug(self):
            logger.debug('DEBUG LOG')

    def _get_suite(self, discover_runner, test_case_cls):
        cls = type(self)
        label = "%s.%s.%s" % (self.__module__, cls.__name__, test_case_cls.__name__)
        suite = discover_runner.build_suite(test_labels=[label])
        # Ensure tests are in alphabetical order, so that test order is
        # deterministic
        suite_cls = type(suite)
        tests = sorted([t for t in suite], key=lambda t: t._testMethodName)
        ordered_suite = suite_cls()
        for test in tests:
            ordered_suite.addTest(test)
        return ordered_suite

    def test_unexpected_success_failfast(self):
        """An unexpected success with --failfast should not stop the test runner"""
        discover_runner = selenosis.DiscoverRunner()
        suite = self._get_suite(discover_runner, self.unexpected_success_failfast)
        runner = discover_runner.test_runner(
            stream=StringIO(),
            failfast=True,
            verbosity=1,
            resultclass=discover_runner.get_resultclass())
        result = runner.run(suite)

        self.assertEqual(result.testsRun, 2)

    def test_debug_sql_unexpected_success_failfast(self):
        """An unexpected success with --failfast should not stop the test runner"""
        discover_runner = selenosis.DiscoverRunner(debug_sql=True)
        suite = self._get_suite(discover_runner, self.unexpected_success_failfast)
        runner = discover_runner.test_runner(
            stream=StringIO(),
            failfast=True,
            verbosity=1,
            resultclass=discover_runner.get_resultclass())
        result = runner.run(suite)

        self.assertEqual(result.testsRun, 2)
