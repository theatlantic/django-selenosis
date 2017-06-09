import os
import tempfile

import django


try:
    import dj_database_url
except ImportError:
    dj_database_url = None


current_dir = os.path.abspath(os.path.dirname(__file__))
temp_dir = tempfile.mkdtemp()


DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

if dj_database_url is not None:
    DATABASES['default'] = dj_database_url.parse(
        os.environ.get('DATABASE_URL', 'sqlite://:memory:'))

SECRET_KEY = 'z-i*xqqn)r0i7leak^#clq6y5j8&tfslp^a4duaywj2$**s*0_'

if django.VERSION > (2, 0):
    MIGRATION_MODULES = {
        'auth': None,
        'contenttypes': None,
        'sessions': None,
    }

try:
    import grappelli  # noqa
except ImportError:
    try:
        import suit  # noqa
    except ImportError:
        INSTALLED_APPS = tuple([])
    else:
        INSTALLED_APPS = tuple(['suit'])
        SUIT_CONFIG = {'CONFIRM_UNSAVED_CHANGES': False}
else:
    INSTALLED_APPS = tuple(['grappelli'])

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(current_dir, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'string_if_invalid': 'INVALID {{ %s }}',
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.template.context_processors.request',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

if django.VERSION < (1, 8):
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.core.context_processors.request',
        'django.contrib.messages.context_processors.messages',
    )
    TEMPLATE_DIRS = (
        os.path.join(current_dir, 'templates'),
    )

if 'suit' in INSTALLED_APPS:
    # django-suit has issues with string_if_invalid,
    # so don't use this setting if testing suit.
    TEMPLATES[0]['OPTIONS'].pop('string_if_invalid')


INSTALLED_APPS += (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_admin_testutils',
)


if django.VERSION >= (1, 10):
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
else:
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

    if django.VERSION > (1, 7):
        MIDDLEWARE_CLASSES += (
            'django.contrib.auth.middleware.SessionAuthenticationMiddleware', )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django_admin_testutils': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}

SITE_ID = 1
ROOT_URLCONF = 'django_admin_testutils.urls'
MEDIA_ROOT = os.path.join(temp_dir, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
DEBUG_PROPAGATE_EXCEPTIONS = True
TEST_RUNNER = 'django_admin_testutils.runner.DiscoverRunner'
