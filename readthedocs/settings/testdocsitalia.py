from __future__ import absolute_import
import os

from .test import CommunityTestSettings


CommunityTestSettings.load_settings(__name__)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'PREFIX': 'docs',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USERNAME': 'postgres',
        'HOST': '',
        'PORT': 5433,
        'PASSWORD': '',
        'NAME': 'test_docsitalia'
    }
}


if not os.environ.get('DJANGO_SETTINGS_SKIP_LOCAL', False):
    try:
        from .test_local_settings import *  # noqa
    except ImportError:
        pass
