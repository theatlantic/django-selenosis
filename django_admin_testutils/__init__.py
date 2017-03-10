# All this craziness is so that we can allow the classes in
# django_admin_testutils.runner to be importable directly from this module, e.g.:
#
#     from django_admin_testutils import DiscoverRunner
#
# without running afoul of the strict import order required by Django 1.9+.
# This implementation is shamelessly stolen from werkzeug's ``__init__.py``.
import pkg_resources
import sys
from types import ModuleType

try:
    __version__ = pkg_resources.get_distribution('django-admin-testutils').version
except pkg_resources.DistributionNotFound:
    __version__ = None

# import mapping to objects in other modules
all_by_module = {
    'django_admin_testutils.selenium': ['SeleniumTestCase', 'SeleniumTestCaseBase'],
    'django_admin_testutils.runner': ['DiscoverRunner'],
    'django_admin_testutils.runtests': ['RunTests'],
    'django_admin_testutils.testcases': [
        'AdminSeleniumTestCase', 'AdminSeleniumTestCaseBase'],
}

# modules that should be imported when accessed as attributes of django_admin_testutils
attribute_modules = frozenset(['settings', 'urls'])

object_origins = {}
for module, items in all_by_module.items():
    for item in items:
        object_origins[item] = module


class module(ModuleType):

    def __dir__(self):
        result = list(new_module.__all__)
        result.extend(('__file__', '__path__', '__doc__', '__all__', '__name__',
                       '__docformat__', '__package__', '__version__'))
        return result

    def __getattr__(self, name):
        if name in object_origins:
            module = __import__(object_origins[name], None, None, [name])
            for extra_name in all_by_module[module.__name__]:
                setattr(self, extra_name, getattr(module, extra_name))
            return getattr(module, name)
        elif name in attribute_modules:
            __import__('django_admin_testutils.' + name)
        return ModuleType.__getattribute__(self, name)


# keep a reference to this module so that it's not garbage collected
old_module = sys.modules[__name__]

# setup the new module and patch it into the dict of loaded modules
new_module = sys.modules[__name__] = module(__name__)
new_module.__dict__.update({
    '__all__': tuple(object_origins) + tuple(attribute_modules),
    '__doc__': __doc__,
    '__file__': __file__,
    '__path__': __path__,
    '__package__': 'django_admin_testutils',
    '__version__': __version__,
    '__docformat__': 'restructuredtext en',
})
