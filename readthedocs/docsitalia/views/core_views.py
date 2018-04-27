# -*- coding: utf-8 -*-
"""Public project views."""

from __future__ import absolute_import
from __future__ import unicode_literals

from django.views.generic import DetailView, ListView
from readthedocs.docsitalia.models import PublisherProject, Publisher
from readthedocs.projects.models import Project


class DocsItaliaHomePage(ListView):  # pylint: disable=too-many-ancestors

    """Docs italia Home Page"""

    model = Project
    template_name = 'docsitalia/docsitalia_homepage.html'

    def get_queryset(self):
        """get queryset"""
        actives = PublisherProject.objects.filter(active=True)
        return Project.objects.filter(publisherproject__in=actives).order_by(
            '-modified_date', '-pub_date'
        )[:24]


class PublisherIndex(DetailView):  # pylint: disable=too-many-ancestors

    """Detail view of :py:class:`Publisher` instances."""

    model = Publisher


class PublisherProjectIndex(DetailView):  # pylint: disable=too-many-ancestors

    """Detail view of :py:class:`PublisherProject` instances."""

    model = PublisherProject
