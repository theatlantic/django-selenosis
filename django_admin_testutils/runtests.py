import os
import sys
import warnings

import django
from django.core.management import (
    BaseCommand, execute_from_command_line, handle_default_options)

try:
    from django.core.management import CommandParser
except ImportError:
    CommandParser = None
    from django.core.management import LaxOptionParser
    from optparse import make_option
else:
    LaxOptionParser = None


class RunTests(object):

    def __init__(self, default_settings_module, default_test_label):
        self.default_settings_module = default_settings_module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', self.default_settings_module)
        self.default_test_label = default_test_label

    def __call__(self, argv=None):
        if argv is None:
            argv = sys.argv[1:]

        warnings.filterwarnings('ignore', module="IPython", category=DeprecationWarning)
        warnings.filterwarnings("ignore", module="distutils")
        try:
            warnings.filterwarnings("ignore", category=ResourceWarning)
        except NameError:
            pass
        warnings.filterwarnings("ignore", "invalid escape sequence", DeprecationWarning)

        default_settings = os.environ.get(
            'DJANGO_SETTINGS_MODULE', self.default_settings_module)
        if CommandParser:
            parser = CommandParser(
                None, usage="%(prog)s [options] [args]", add_help=False)
            parser.add_argument('--settings', default=default_settings)
            parser.add_argument('--pythonpath')
            parser.add_argument(
                '--testrunner', action='store',
                default='django_admin_testutils.DiscoverRunner')
            parser.add_argument('args', nargs='*')
            options, remaining_args = parser.parse_known_args(argv)
        else:
            from django_admin_testutils.runner import DiscoverRunner

            option_list = BaseCommand.option_list + (
                make_option('--noinput',
                    action='store_false', dest='interactive', default=True,
                    help='Tells Django to NOT prompt the user for input of any kind.'),
                make_option('--failfast',
                    action='store_true', dest='failfast', default=False,
                    help='Tells Django to stop running the test suite after first '
                         'failed test.'),
                make_option('--testrunner',
                    action='store', dest='testrunner',
                    help='Tells Django to use specified test runner class instead of '
                         'the one specified by the TEST_RUNNER setting.'),
                make_option('--liveserver',
                    action='store', dest='liveserver', default=None,
                    help='Overrides the default address where the live server (used '
                         'with LiveServerTestCase) is expected to run from. The '
                         'default value is localhost:8081.'),
            ) + DiscoverRunner.option_list
            parser = LaxOptionParser(usage="%prog [options] [args]",
                option_list=option_list)
            options, remaining_args = parser.parse_args(argv)
            options.testrunner = 'django_admin_testutils.DiscoverRunner'
            options.args = remaining_args
            remaining_args = []

        handle_default_options(options)
        test_labels = options.args or [self.default_test_label]
        flags = ['--testrunner=%s' % options.testrunner] + remaining_args

        if hasattr(options, 'selenium'):
            flags.insert(0, '--selenium=%s' % ','.join(options.selenium))

        # Ignore a python 3.6 DeprecationWarning in ModelBase.__new__ that isn't
        # fixed in Django 1.x
        if sys.version_info > (3, 6) and django.VERSION < (2,):
            warnings.filterwarnings(
                "ignore", "__class__ not set defining", DeprecationWarning)

        from django.conf import settings

        if 'grappelli' in settings.INSTALLED_APPS:
            # Grappelli uses the deprecated django.conf.urls.patterns, but we
            # don't want this to fail our tests.
            warnings.filterwarnings("ignore", "django.conf.urls.patterns", Warning)

            if django.VERSION < (1, 5):
                # Ignore warning with grappelli and deprecated url templatetag
                warnings.filterwarnings("ignore", "The syntax for the url", Warning)

            if django.VERSION[:2] == (1, 7):
                warnings.filterwarnings(
                    "ignore", "The django.contrib.admin.util module", Warning)

        self.execute(flags, test_labels)

    def execute(self, flags, test_labels):
        execute_from_command_line(sys.argv[:1] + ['test'] + flags + test_labels)
