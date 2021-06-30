import os
import tempfile


current_dir = os.path.abspath(os.path.dirname(__file__))
temp_dir = tempfile.mkdtemp()


DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
SECRET_KEY = 'z-i*xqqn)r0i7leak^#clq6y5j8&tfslp^a4duaywj2$**s*0_'

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
    'selenosis',
)


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'selenosis': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}

SITE_ID = 1
ROOT_URLCONF = 'selenosis.urls'
MEDIA_ROOT = os.path.join(temp_dir, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
DEBUG_PROPAGATE_EXCEPTIONS = True
TEST_RUNNER = 'selenosis.runner.DiscoverRunner'
