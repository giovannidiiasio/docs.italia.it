from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class DocsitaliaConfig(AppConfig):
    name = 'docsitalia'

    def ready(self):
        import readthedocs.docsitalia.signals # noqa
