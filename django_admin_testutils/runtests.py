import os
import sys
import warnings

import django
from django.core.management import (
    CommandParser, execute_from_command_line, handle_default_options)


class RunTests(object):

    def __init__(self, default_settings_module, default_test_label):
        self.default_settings_module = default_settings_module
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

        parser = CommandParser(
            None, usage="%(prog)s [options] [args]", add_help=False)
        default_settings = os.environ.get(
            'DJANGO_SETTINGS_MODULE', self.default_settings_module)
        parser.add_argument('--settings', default=default_settings)
        parser.add_argument('--pythonpath')
        parser.add_argument(
            '--testrunner', action='store',
            default='django_admin_testutils.DiscoverRunner')
        parser.add_argument('args', nargs='*')

        options, remaining_args = parser.parse_known_args(argv)
        handle_default_options(options)

        test_labels = options.args or [self.default_test_label]
        flags = ['--testrunner=%s' % options.testrunner] + remaining_args

        # Ignore a python 3.6 DeprecationWarning in ModelBase.__new__ that isn't
        # fixed in Django 1.x
        if sys.version_info > (3, 6) and django.VERSION < (2,):
            warnings.filterwarnings(
                "ignore", "__class__ not set defining", DeprecationWarning)

        # Ignore a deprecation warning in distutils.spawn for python 3.4
        if sys.version_info[:2] == (3, 4):
            warnings.filterwarnings("ignore", "the imp module", Warning)

        from django.conf import settings

        if 'grappelli' in settings.INSTALLED_APPS:
            # Grappelli uses the deprecated django.conf.urls.patterns, but we
            # don't want this to fail our tests.
            warnings.filterwarnings("ignore", "django.conf.urls.patterns", Warning)

        self.execute(flags, test_labels)

    def execute(self, flags, test_labels):
        execute_from_command_line(sys.argv[:1] + ['test'] + flags + test_labels)
