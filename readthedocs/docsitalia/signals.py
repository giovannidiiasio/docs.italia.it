# -*- coding: utf-8 -*-
"""Signals for the docsitalia app."""

from __future__ import absolute_import

import logging

from django.dispatch import receiver

from readthedocs.doc_builder.signals import finalize_sphinx_context_data
from readthedocs.oauth.models import RemoteRepository
from readthedocs.projects.signals import project_import
from readthedocs.restapi.client import api as apiv2
from .models import PublisherProject


log = logging.getLogger(__name__) # noqa


@receiver(project_import)
def on_project_import(sender, **kwargs): # noqa
    """Connect a Project to its PublisherProject"""
    project = sender

    try:
        remote = RemoteRepository.objects.get(project=project)
    except RemoteRepository.DoesNotExist:
        log.error('Missing RemoteRepository for project {}'.format(project))
        return

    pub_projects = PublisherProject.objects.filter(
        metadata__documents__contains=[remote.html_url]
    )
    for pub_proj in pub_projects:
        pub_proj.projects.add(project)


@receiver(finalize_sphinx_context_data)
def add_sphinx_context_data(sender, **kwargs):
    data = kwargs.get('data')
    build_env = kwargs.get('build_env')
    subprojects = (apiv2.project(build_env.project.pk)
                   .subprojects()
                   .get()['subprojects'])
    data['subprojects'] = subprojects
