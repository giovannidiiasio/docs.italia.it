from __future__ import absolute_import
from django.conf.urls import url

from .views.core_views import PublisherIndex, DocsItaliaHomePage, PublisherProjectIndex
from .views.core_views import DocsItaliaHomePage, PublisherIndex, PublisherProjectIndex


urlpatterns = [
    url(
        r'^$',
        DocsItaliaHomePage.as_view(),
        name='docsitalia_homepage'
    ),
    url(
        r'^(?P<slug>[-\w]+)$',
        PublisherIndex.as_view(),
        name='publisher_detail'
    ),
    url(
        r'^(?P<publisherslug>[-\w]+)/(?P<slug>[-\w]+)$',
        PublisherProjectIndex.as_view(),
        name='publisher_project_detail'
    ),
]
