from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class DocsItaliaConfig(AppConfig):
    name = 'readthedocs.docsitalia'
    verbose_name = 'Docs Italia'

    def ready(self):
        import readthedocs.docsitalia.signals # noqa
