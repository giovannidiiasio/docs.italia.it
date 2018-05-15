"""Build and Version class model Managers"""

from __future__ import absolute_import

from django.conf import settings
from django.db import models

from .constants import BRANCH, TAG
from .querysets import VersionQuerySet
from readthedocs.core.utils.extend import (SettingsOverrideObject,
                                           get_override_class)


__all__ = ['VersionManager']


class VersionManagerBase(models.Manager):

    """
    Version manager for manager only queries.

    For queries not suitable for the :py:cls:`VersionQuerySet`, such as create
    queries.
    """

    @classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        # This is overridden because :py:meth:`models.Manager.from_queryset`
        # uses `inspect` to retrieve the class methods, and the proxy class has
        # no direct members.
        queryset_class = get_override_class(
            VersionQuerySet,
            VersionQuerySet._default_class  # pylint: disable=protected-access
        )
        return super(VersionManagerBase, cls).from_queryset(queryset_class, class_name)

    def create_stable(self, **kwargs):
        defaults = {
            'slug': settings.STABLE,
            'verbose_name': settings.STABLE_VERBOSE_NAME,
            'machine': True,
            'active': True,
            'identifier': settings.STABLE,
            'type': TAG,
        }
        defaults.update(kwargs)
        return self.create(**defaults)

    def create_latest(self, **kwargs):
        defaults = {
            'slug': settings.LATEST,
            'verbose_name': settings.LATEST_VERBOSE_NAME,
            'machine': True,
            'active': True,
            'identifier': settings.LATEST,
            'type': BRANCH,
        }
        defaults.update(kwargs)
        return self.create(**defaults)


class VersionManager(SettingsOverrideObject):
    _default_class = VersionManagerBase
    _override_setting = 'VERSION_MANAGER'
