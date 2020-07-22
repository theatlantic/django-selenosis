from __future__ import print_function

import logging
import unittest

import six
import django.test.runner

import selenosis


DJANGO_NATIVE_TAG_SUPPORT = hasattr(django.test.runner, 'filter_tests_by_tags')


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

    def test_tags(self):
        """Backported --tags= functionality should only include tests with @tag"""
        if DJANGO_NATIVE_TAG_SUPPORT:
            raise unittest.SkipTest('skipping test of native @tag implementation')
        runner = selenosis.DiscoverRunner(tags=['tag1'])
        suite = self._get_suite(runner, self.tag_decorator)
        self.assertEqual(suite.countTestCases(), 1)
        test = [t for t in suite][0]
        self.assertEqual(test._testMethodName, 'test_tag1')

    def test_exclude_tags(self):
        """Backported --exclude-tags= functionality should exclude tests with @tag"""
        if DJANGO_NATIVE_TAG_SUPPORT:
            raise unittest.SkipTest('skipping test of native @tag implementation')
        runner = selenosis.DiscoverRunner(exclude_tags=['tag1'])
        suite = self._get_suite(runner, self.tag_decorator)
        self.assertEqual(suite.countTestCases(), 1)
        test = [t for t in suite][0]
        self.assertEqual(test._testMethodName, 'test_tag2')

    def test_unexpected_success_failfast(self):
        """An unexpected success with --failfast should not stop the test runner"""
        discover_runner = selenosis.DiscoverRunner()
        suite = self._get_suite(discover_runner, self.unexpected_success_failfast)
        runner = discover_runner.test_runner(
            stream=six.StringIO(),
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
            stream=six.StringIO(),
            failfast=True,
            verbosity=1,
            resultclass=discover_runner.get_resultclass())
        result = runner.run(suite)

        self.assertEqual(result.testsRun, 2)
