import os

from .base import *  # noqa
from .env import env

SECRET_KEY = env.get_credential('DJANGO_SECRET_KEY')

DEBUG = False
TEMPLATE_DEBUG = False

# TODO(jmcarp) Update after configuring DNS
ALLOWED_HOSTS = ['*']

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}


try:
    from .local import *  # noqa
except ImportError:
    pass
