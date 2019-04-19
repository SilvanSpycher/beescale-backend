from .settings import *

# Use InMemory EMAIL_BACKEND when testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable sentry monitoring when running tests
RAVEN_CONFIG = None
for app in INSTALLED_APPS:
    if app.startswith('raven.'):
        INSTALLED_APPS.pop(INSTALLED_APPS.index(app))

# propagate overrides
THUMBNAIL_DEBUG = DEBUG
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
