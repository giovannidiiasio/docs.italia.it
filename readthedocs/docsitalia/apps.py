# -*- coding: utf-8 -*-
"""AppConfig for the docsitalia app."""

from django.apps import AppConfig


class DocsItaliaConfig(AppConfig):
    name = 'readthedocs.docsitalia'
    verbose_name = 'Docs Italia'

    def ready(self):
        import readthedocs.docsitalia.signals # noqa
