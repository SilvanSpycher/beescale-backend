# Logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_LOGFILE_PATH = os.path.join(BASE_DIR, 'django.log')
LOGFILE_PATH = os.environ.get('LOGFILE_PATH', None) or DEFAULT_LOGFILE_PATH

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'colored': {
            '()': 'coloredlogs.ColoredFormatter',
            'format': '[%(asctime)s] %(name)s %(levelname)-8s %(module)s %(message)s',
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'hostname': {
            '()': 'coloredlogs.HostNameFilter',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'filters': ['hostname']
        },
        'log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOGFILE_PATH,
            'formatter': 'default',
            'filters': ['require_debug_false'],
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['console', 'mail_admins', 'log_file'],
            'level': 'INFO',
            'propagate': False
        },
    },
    # you can also shortcut 'loggers' and just configure logging for EVERYTHING at once
    # 'root': {
    #     'handlers': ['console', 'mail_admins', 'log_file'],
    #     'level': 'INFO'
    # },
}
