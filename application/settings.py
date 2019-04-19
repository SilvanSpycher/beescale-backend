import datetime
import os
import sys
from distutils.util import strtobool

import raven
from dotenv import load_dotenv

from application.env_utils import load_yaml_env

# --- START CUSTOMIZING HERE ---

ADMINS = [('Project Name', 'webdev+[PROJECT-NAME]@smartfactory.ch')]
USE_MEMCACHE = False

# --- STOP CUSTOMIZING ---

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)
ENV = load_yaml_env()

DEBUG = ENV.get('DEBUG', False)
HOST = ENV.HOST
ALLOWED_HOSTS = ENV.get('ALLOWED_HOSTS', HOST)

# The secret is being read from .env or generated if not yet present
SECRET_KEY = ENV.get_password('SECRET_KEY', length=50)

# Application definition
INSTALLED_APPS = [
    'template_support',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'raven.contrib.django.raven_compat',
    'rest_framework',
    'drf_yasg',
    'webpack_loader',

    # Start registering your project apps here
    'application'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'application.wsgi.application'

# Database configuration using .env file
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ENV.DATABASE.NAME,
        'USER': ENV.DATABASE.USERNAME,
        'PASSWORD': ENV.DATABASE.PASSWORD,
        'HOST': ENV.DATABASE.get('HOST', '127.0.0.1'),
        'ATOMIC_REQUESTS': True
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Zurich'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Caching
if USE_MEMCACHE:
    try:
        import pylibmc
    except ImportError:
        print(f'You enabled Memcache by setting USE_MEMCACHE = True.\n'
              f'To use this backend, please install pylibmc using pipenv install pylibmc.')
        sys.exit(1)

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': '127.0.0.1:11211'
        }
    }
    KEY_PREFIX = HOST

# Configure Sentry
RAVEN_CONFIG = {
    'dsn': ENV.SENTRY.get('DSN', None),
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ),
    'SEARCH_PARAM': 'q',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_VERSION': 'v1',
    'COERCE_DECIMAL_TO_STRING': False,
    'NON_FIELD_ERRORS_KEY': '__all__',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer'
}

# Swagger (API Docs)
SWAGGER_SETTINGS = {
    'API_VERSION': '1.0',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'SHOW_REQUEST_HEADERS': True,
    'DOC_EXPANSION': 'list',
    'USE_SESSION_AUTH': True,
    'PERSIST_AUTH': True,
    'REFETCH_SCHEMA_WITH_AUTH': True
}
LOGIN_URL = '/admin/login'
LOGOUT_URL = '/admin/logout'

# Configure logging
try:
    from .logging import LOGGING
except ImportError:
    pass

# ENV.persist_to_dotenv()
ENV.persist()

# make sure certain constraints are being followed
if not ENV.SENTRY.get('SKIP', False) and (RAVEN_CONFIG is not None and RAVEN_CONFIG['dsn'] is None):
    print(f'You did not configure a SENTRY_DSN variable in your .env file, aborting application startup.')
    sys.exit(1)
