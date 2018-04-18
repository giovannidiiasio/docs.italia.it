# -*- coding: utf-8 -*-
"""Admin for the docsitalia app."""

from django.contrib import admin

from .models import Publisher, PublisherProject

admin.site.register(Publisher)
admin.site.register(PublisherProject)
