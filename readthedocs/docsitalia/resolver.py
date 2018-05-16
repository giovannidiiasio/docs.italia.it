"""Override RTD URL resolver"""

from django.conf import settings

from readthedocs.core.resolver import ResolverBase


class ItaliaResolver(ResolverBase):

    """Custom path resolver for built documentation

    Resolves to public domain without use of subdomains or /doc/* paths
    """

    def base_resolve_path(self, project_slug, filename, version_slug=None,
                          language=None, private=False, single_version=None,
                          subproject_slug=None, subdomain=None, cname=None):

        from readthedocs.projects.models import Project
        url = u'/{publisher_slug}/{base_project_slug}/{project_slug}/'

        if subproject_slug:
            url += u'projects/{subproject_slug}/'

        if single_version:
            url += u'{filename}'
        else:
            url += u'{language}/{version_slug}/{filename}'

        project = Project.objects.get(slug=project_slug)
        base_project = project.publisherproject_set.all().first()
        return url.format(
            project_slug=project_slug, filename=filename,
            base_project_slug=base_project.slug, publisher_slug=base_project.publisher.slug,
            version_slug=version_slug, language=language,
            single_version=single_version, subproject_slug=subproject_slug,
        )

    def resolve_domain(self, project, private=None):
        canonical_project = self._get_canonical_project(project)
        domain = canonical_project.domains.filter(canonical=True).first()
        if domain:
            return domain.domain
        return getattr(settings, 'PUBLIC_DOMAIN')

    def resolve(self, *args, **kwargs):
        kwargs['protocol'] = getattr(settings, 'PUBLIC_PROTO', 'https')
        return super(ItaliaResolver, self).resolve(*args, **kwargs)
