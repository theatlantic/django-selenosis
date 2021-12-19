import os
import sys
import warnings


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

        # Ignore a deprecation warning in distutils.spawn for python 3.4+
        warnings.filterwarnings("ignore", "the imp module", Warning)

        warnings.filterwarnings('once', 'Selenium support for PhantomJS', Warning)

        from django.core.management import CommandParser, handle_default_options

        parser = CommandParser(usage="%(prog)s [options] [args]", add_help=False)

        default_settings = os.environ.get(
            'DJANGO_SETTINGS_MODULE', self.default_settings_module)
        parser.add_argument('--settings', default=default_settings)
        parser.add_argument('--pythonpath')
        parser.add_argument(
            '--testrunner', action='store',
            default='selenosis.DiscoverRunner')
        parser.add_argument('args', nargs='*')

        options, remaining_args = parser.parse_known_args(argv)
        handle_default_options(options)

        test_labels = options.args or [self.default_test_label]
        flags = ['--testrunner=%s' % options.testrunner] + remaining_args

        self.execute(flags, test_labels)

    def execute(self, flags, test_labels):
        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv[:1] + ['test'] + flags + test_labels)
