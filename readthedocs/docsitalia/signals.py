# -*- coding: utf-8 -*-
"""Signals for the docsitalia app."""

from __future__ import absolute_import

import logging

from django.dispatch import receiver

from readthedocs.oauth.models import RemoteRepository
from readthedocs.projects.signals import project_import

from .models import PublisherProject


log = logging.getLogger(__name__)


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
