from __future__ import absolute_import
from builtins import str
import logging
import json

from readthedocs.oauth.services.github import GitHubService
from readthedocs.oauth.models import RemoteOrganization

from ..models import (
    Publisher, validate_publisher_metadata, validate_projects_metadata)

log = logging.getLogger(__name__)

METADATA_BASE_URL = (
    'https://raw.githubusercontent.com/{org}/{repo}/master/{settings}'
)


class DocsItaliaGithubService(GitHubService):
    def sync(self):
        """Sync organizations."""
        self.sync_organizations()

    def get_metadata_for_organization(self, org, repo, settings):
        # FIXME: error handling
        url = METADATA_BASE_URL.format(
            org=org, repo=repo, settings=settings)
        return self.paginate(url)

    def sync_organizations(self):
        """Sync organizations from GitHub API."""
        try:
            orgs = self.paginate('https://api.github.com/user/orgs')
            for org in orgs:
                org_resp = self.get_session().get(org['url'])
                org_obj = self.create_organization(org_resp.json())

                # we ingest only whitelisted organizations
                if not org_obj:
                    continue

                publisher = Publisher.objects.get(
                    organizations=org_obj, active=True)
                publisher_settings = self.get_metadata_for_organization(
                    org=org_obj.slug,
                    repo=publisher.config_repo_name,
                    settings='publisher_settings.yml')

                if not publisher_settings:
                    log.debug(
                        'Syncing GitHub organizations: '
                        'no publisher metadata for {}'.format(
                            publisher))
                    continue

                try:
                    publisher_metadata = validate_publisher_metadata(
                        org_obj, publisher_settings)
                except ValueError:
                    log.debug(
                        'Syncing GitHub organizations: '
                        'invalid publisher metadata for {}'.format(
                            publisher))
                    continue

                projects_settings = self.get_metadata_for_organization(
                    org=org_obj.slug,
                    repo=publisher.config_repo_name,
                    settings='projects_settings.yml')

                if not projects_settings:
                    log.debug(
                        'Syncing GitHub organizations: '
                        'no projects metadata for {}'.format(
                            publisher))
                    continue

                try:
                    projects_metadata = validate_projects_metadata(
                        org_obj, projects_settings)
                except ValueError:
                    log.debug(
                        'Syncing GitHub organizations: '
                        'invalid projects metadata for {}'.format(
                            publisher))
                    continue

                publisher.metadata = publisher_metadata
                publisher.projects_metadata = projects_metadata
                publisher.save()
                publisher.create_projects_from_metadata(projects_metadata)

                # Add repos
                # TODO ?per_page=100
                org_repos = self.paginate(
                    '{org_url}/repos'.format(org_url=org['url'])
                )

                for repo in org_repos:
                    self.create_repository(repo, organization=org_obj)
        except (TypeError, ValueError) as e:
            log.error('Error syncing GitHub organizations: %s',
                      str(e), exc_info=True)
            raise Exception('Could not sync your GitHub organizations, '
                            'try reconnecting your account')

    def create_organization(self, fields):
        """
        Update or create remote organization from GitHub API response.

        :param fields: dictionary response of data from API
        :rtype: Publisher
        """
        # TODO: is this the right one?
        name = fields.get('name')
        try:
            publisher = Publisher.objects.get(
                name=name,
                active=True)
        except Publisher.DoesNotExist:
            return None

        try:
            organization = RemoteOrganization.objects.get(
                slug=fields.get('login'),
                users=self.user,
                account=self.account,
            )
        except RemoteOrganization.DoesNotExist:
            # TODO: fun fact: slug is not unique
            organization = RemoteOrganization.objects.create(
                slug=fields.get('login'),
                account=self.account,
            )
            organization.users.add(self.user)

        publisher.organizations.add(organization)

        organization.url = fields.get('html_url')
        organization.name = name
        organization.email = fields.get('email')
        organization.avatar_url = fields.get('avatar_url')
        if not organization.avatar_url:
            organization.avatar_url = self.default_org_avatar_url
        organization.json = json.dumps(fields)
        organization.account = self.account
        organization.save()

        return organization
