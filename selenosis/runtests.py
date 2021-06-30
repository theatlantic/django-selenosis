import os
import sys
import warnings


class RunTests:

    def __init__(self, default_settings_module, default_test_label):
        self.default_settings_module = default_settings_module
        self.default_test_label = default_test_label

    def __call__(self, argv=None):
        from django.conf import settings
        from django.core.management import CommandParser, handle_default_options

        if argv is None:
            argv = sys.argv[1:]

        try:
            warnings.filterwarnings("ignore", category=ResourceWarning)
        except NameError:
            pass

        warnings.filterwarnings('ignore', module="IPython", category=DeprecationWarning)
        warnings.filterwarnings("ignore", module="distutils")
        warnings.filterwarnings("ignore", "invalid escape sequence", DeprecationWarning)
        warnings.filterwarnings("ignore", "the imp module", Warning)
        warnings.filterwarnings('once', 'Selenium support for PhantomJS', Warning)

        default_settings = os.environ.get('DJANGO_SETTINGS_MODULE', self.default_settings_module)
        parser = CommandParser(usage="%(prog)s [options] [args]", add_help=False)
        parser.add_argument('--settings', default=default_settings)
        parser.add_argument('--pythonpath')
        parser.add_argument('--testrunner', action='store', default='selenosis.DiscoverRunner')
        parser.add_argument('args', nargs='*')

        options, remaining_args = parser.parse_known_args(argv)
        handle_default_options(options)

        test_labels = options.args or [self.default_test_label]
        flags = ['--testrunner=%s' % options.testrunner] + remaining_args

        if 'grappelli' in settings.INSTALLED_APPS:
            # Grappelli uses the deprecated django.conf.urls.patterns, but we
            # don't want this to fail our tests.
            warnings.filterwarnings("ignore", "django.conf.urls.patterns", Warning)

        self.execute(flags, test_labels)

    def execute(self, flags, test_labels):
        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv[:1] + ['test'] + flags + test_labels)
