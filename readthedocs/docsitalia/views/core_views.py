# -*- coding: utf-8 -*-
"""Public project views."""

from __future__ import absolute_import
from __future__ import unicode_literals

from django.shortcuts import render
from readthedocs.docsitalia.models import PublisherProject, Publisher
from django.views.generic import DetailView, ListView
from readthedocs.projects.models import Project


class DocsItaliaHomePage(ListView):

    """Docs italia Home Page"""

    model = Project
    template_name = 'docsitalia/docsitalia_homepage.html'

    def get_context_data(self, **kwargs):
        context = super(DocsItaliaHomePage, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        actives = PublisherProject.objects.filter(active=True)
        return Project.objects.filter( # this will eventually become most viewed this month
            publisherproject__in=actives).order_by('-modified_date', '-pub_date'
        )[:10]


class PublisherIndex(DetailView):

    """Detail view of :py:class:`Publisher` instances."""

    model = Publisher

    def get_context_data(self, **kwargs):
        context = super(PublisherIndex, self).get_context_data(**kwargs)
        return context


class PublisherProjectIndex(DetailView):

    """Detail view of :py:class:`PublisherProject` instances."""

    model = PublisherProject

    def get_context_data(self, **kwargs):
        context = super(PublisherProjectIndex, self).get_context_data(**kwargs)
        return context
