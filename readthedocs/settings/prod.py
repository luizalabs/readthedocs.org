"""Production settings."""
from __future__ import absolute_import

from decouple import config

from .base import CommunityBaseSettings


class CommunityProdSettings(CommunityBaseSettings):
    """Settings for production."""

    PRODUCTION_DOMAIN = config('PRODUCTION_DOMAIN')
    WEBSOCKET_HOST = config('WEBSOCKET_HOST')

    @property
    def DATABASES(self):  # noqa
        return {
            'default': {
                'ENGINE': config('DATABASE_ENGINE'),
                'NAME': config('MYSQL_DATABASE_NAME'),
                'USER': config('MYSQL_USER', ''),
                'PASSWORD': config('MYSQL_PASSWORD', ''),
                'HOST': config('MYSQL_HOST', ''),
                'PORT': config('MYSQL_PORT', default=3306, cast=int),
            }
        }

    DONT_HIT_DB = False

    SESSION_COOKIE_DOMAIN = config('SESSION_COOKIE_DOMAIN', default=None)
    CACHE_BACKEND = 'dummy://'

    SLUMBER_USERNAME = config('SLUMBER_USERNAME')
    SLUMBER_PASSWORD = config('SLUMBER_PASSWORD')
    SLUMBER_API_HOST = config('SLUMBER_API_HOST')

    BROKER_URL = config('BROKER_URL')
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
    CELERY_ALWAYS_EAGER = config('CELERY_ALWAYS_EAGER', default=True)

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    FILE_SYNCER = 'readthedocs.builds.syncers.LocalSyncer'

    NGINX_X_ACCEL_REDIRECT = True

    @property
    def LOGGING(self):  # noqa - avoid pep8 N802
        logging = super(CommunityProdSettings, self).LOGGING
        logging['formatters']['default']['format'] = (
            '[%(asctime)s] ' + self.LOG_FORMAT
        )
        logging['handlers']['logentries'] = {
            'token': config('LOGENTRIES_TOKEN'),
            'class': 'logentries.LogentriesHandler'
        }
        logging['loggers']['readthedocs']['handlers'] += ['logentries']
        return logging


CommunityProdSettings.load_settings(__name__)
