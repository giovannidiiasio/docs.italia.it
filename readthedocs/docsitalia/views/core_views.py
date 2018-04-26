# -*- coding: utf-8 -*-
"""Public project views."""

from __future__ import absolute_import
from __future__ import unicode_literals

from django.views.generic import DetailView, ListView
from readthedocs.docsitalia.models import PublisherProject, Publisher
from readthedocs.projects.models import Project


class DocsItaliaHomePage(ListView):

    """Docs italia Home Page"""

    model = Project
    template_name = 'docsitalia/docsitalia_homepage.html'

    def get_queryset(self):
        """get queryset"""
        actives = PublisherProject.objects.filter(active=True)
        return Project.objects.filter( # this will eventually become most viewed this month
            publisherproject__in=actives).order_by('-modified_date', '-pub_date'
        )[:24]


class PublisherIndex(DetailView):

    """Detail view of :py:class:`Publisher` instances."""

    model = Publisher


class PublisherProjectIndex(DetailView):

    """Detail view of :py:class:`PublisherProject` instances."""

    model = PublisherProject
