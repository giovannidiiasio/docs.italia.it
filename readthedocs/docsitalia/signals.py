from __future__ import absolute_import
from django.dispatch import receiver

from readthedocs.projects.signals import project_import

from .models import PublisherProject


@receiver(project_import)
def on_project_import(sender, **kwargs):
    project = sender

    repo_url = project.remoterepository.html_url

    pub_projects = PublisherProject.objects.filter(
        metadata__contains={'repo_url': repo_url}
    )
    for pub_proj in pub_projects:
        pub_proj.projects.add(project)
