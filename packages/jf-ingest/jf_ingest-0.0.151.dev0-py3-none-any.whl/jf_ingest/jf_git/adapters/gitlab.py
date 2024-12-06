from datetime import datetime
from typing import Any, Dict, Generator, List, Optional

from jf_ingest.config import GitConfig
from jf_ingest.jf_git.adapters import GitAdapter
from jf_ingest.jf_git.clients.gitlab import GitlabClient
from jf_ingest.jf_git.standardized_models import (
    StandardizedBranch,
    StandardizedCommit,
    StandardizedOrganization,
    StandardizedPullRequest,
    StandardizedPullRequestMetadata,
    StandardizedRepository,
    StandardizedTeam,
    StandardizedUser,
)


class GitlabAdapter(GitAdapter):

    def __init__(self, config: GitConfig):
        self.config = config
        self.client = GitlabClient(auth_config=config.git_auth_config)
        self.group_id_to_full_path: Dict[str, str] = {}

    def get_api_scopes(self) -> str:
        """Return the list of API Scopes. This is useful for Validation

        Returns:
            str: A string of API scopes we have, given the adapters credentials
        """
        raise NotImplementedError()

    @staticmethod
    def _get_group_id_from_gid(gitlab_gid: str) -> str:
        """Helper function.
        The Gitlab GQL returns Group (Organization) IDs with this weird GID format.
        All we care about is the number trailing at the end.
        Gitlab Format: gid://gitlab/Group/{ID_NUMBER}
        """
        return gitlab_gid.split('gid://gitlab/Group/')[1]

    def get_group_full_path_from_id(self, group_id: str) -> str:
        if group_id not in self.group_id_to_full_path:
            _, full_path, _ = self.client.get_organization_name_full_path_and_url(login=group_id)
            self.group_id_to_full_path[group_id] = full_path

        return self.group_id_to_full_path[group_id]

    def get_organizations(self) -> List[StandardizedOrganization]:
        """Get the list of organizations the adapter has access to

        Returns:
            List[StandardizedOrganization]: A list of standardized organizations within this Git Instance
        """
        orgs: List[StandardizedOrganization] = []
        if not self.config.discover_organizations:
            for group_id in self.config.git_organizations:
                name, full_path, url = self.client.get_organization_name_full_path_and_url(
                    login=group_id
                )
                self.group_id_to_full_path[group_id] = full_path
                orgs.append(
                    StandardizedOrganization(id=group_id, name=name, login=group_id, url=url)
                )
        else:
            # Discover Orgs
            for api_org in self.client.get_organizations():
                group_id = self._get_group_id_from_gid(api_org['id'])
                full_path = api_org['fullPath']
                self.group_id_to_full_path[group_id] = full_path
                orgs.append(
                    StandardizedOrganization(
                        id=group_id, name=api_org['name'], login=group_id, url=api_org['webUrl']
                    )
                )

        return orgs

    def get_users(
        self, standardized_organization: StandardizedOrganization, limit: Optional[int] = None
    ) -> Generator[StandardizedUser, None, None]:
        """Get the list of users in a given Git Organization

        Args:
            standardized_organization (StandardizedOrganization): A standardized Git Organization Object

        Returns:
            List[StandardizedUser]: A standardized User Object
            limit (int, optional): When provided, the number of items returned is limited.
                Useful for the validation use case, where we want to just verify we can pull PRs.
                Defaults to None.
        """
        raise NotImplementedError()

    def get_teams(
        self, standardized_organization: StandardizedOrganization, limit: Optional[int] = None
    ) -> Generator[StandardizedTeam, None, None]:
        """Get the list of teams in a given Git Organization

        Args:
            standardized_organization (StandardizedOrganization): A standardized Git Organization Object

        Returns:
            List[StandardizedUser]: A standardized Team Object
            limit (int, optional): When provided, the number of items returned is limited.
                Useful for the validation use case, where we want to just verify we can pull PRs.
                Defaults to None.
        """
        raise NotImplementedError()

    def get_repos(
        self,
        standardized_organization: StandardizedOrganization,
    ) -> Generator[StandardizedRepository, None, None]:
        """Get a list of standardized repositories within a given organization

        Args:
            standardized_organization (StandardizedOrganization): A standardized organization

        Returns:
            List[StandardizedRepository]: A list of standardized Repositories
        """
        raise NotImplementedError()

    def get_commits_for_default_branch(
        self,
        standardized_repo: StandardizedRepository,
        limit: Optional[int] = None,
        pull_since: Optional[datetime] = None,
        pull_until: Optional[datetime] = None,
    ) -> Generator[StandardizedCommit, None, None]:
        """For a given repo, get all the commits that are on the Default Branch.

        Args:
            standardized_repo (StandardizedRepository): A standard Repository object
            limit (int): limit the number of commit objects we will yield
            pull_since (datetime): filter commits to be newer than this date
            pull_until (datetime): filter commits to be older than this date

        Returns:
            List[StandardizedCommit]: A list of standardized commits
        """
        raise NotImplementedError()

    def get_branches_for_repo(
        self,
        standardized_repo: StandardizedRepository,
        pull_branches: Optional[bool] = False,
    ) -> Generator[StandardizedBranch, None, None]:
        """Function for pulling branches for a repository. By default, pull_branches will run as False,
        so we will only process the default branch. If pull_branches is true, than we will pull all
        branches in this repository

        Args:
            standardized_repo (StandardizedRepository): A standardized repo, which hold info about the default branch.
            pull_branches (bool): A boolean flag. If True, pull all branches available on Repo. If false, only process the default branch. Defaults to False.

        Yields:
            StandardizedBranch: A Standardized Branch Object
        """
        raise NotImplementedError()

    def get_commits_for_branches(
        self,
        standardized_repo: StandardizedRepository,
        branches: List[StandardizedBranch],
        pull_since: Optional[datetime] = None,
        pull_until: Optional[datetime] = None,
    ) -> Generator[StandardizedCommit, None, None]:
        """For a given repo, get all the commits that are on the included branches.
        Included branches are found by crawling across the branches pulled/available
        from get_filtered_branches

        Args:
            standardized_repo (StandardizedRepository): A standard Repository object
            pull_since (datetime): A date to pull from
            pull_until (datetime): A date to pull up to

        Returns:
            List[StandardizedCommit]: A list of standardized commits
        """
        raise NotImplementedError()

    def get_pr_metadata(
        self,
        standardized_repo: StandardizedRepository,
        limit: Optional[int] = None,
        pr_pull_from_date: Optional[datetime] = None,
    ) -> Generator[StandardizedPullRequestMetadata, None, None]:
        """Get all PRs, but only included the bare necesaties

        Args:
            standardized_repo (StandardizedRepository): A standardized repository
            limit (int, optional): When provided, the number of items returned is limited.
                Useful for the validation use case, where we want to just verify we can pull PRs.
                Defaults to None.
            pr_pull_from_date: This is currently only used by the GithubAdapter. Probably won't be useful for this adapter

        Returns:
            List[StandardizedPullRequest]: A list of standardized PRs
        """
        raise NotImplementedError()

    def git_provider_pr_endpoint_supports_date_filtering(self) -> bool:
        """Returns a boolean on if this PR supports time window filtering.
        So far, Github DOES NOT support this (it's adapter will return False)
        but ADO does support this (it's adapter will return True)

        Returns:
            bool: A boolean on if the adapter supports time filtering when searching for PRs
        """
        return True

    def get_prs(
        self,
        standardized_repo: StandardizedRepository,
        pull_files_for_pr: bool = False,
        hash_files_for_prs: bool = False,
        limit: Optional[int] = None,
        start_cursor: Optional[Any] = None,
        start_window: Optional[datetime] = None,
        end_window: Optional[datetime] = None,
    ) -> Generator[StandardizedPullRequest, None, None]:
        """Get the list of standardized Pull Requests for a Standardized Repository.

        Args:
            standardized_repo (StandardizedRepository): A standardized repository
            pull_files_for_pr (bool): When provided, we will pull file metadata for all PRs
            hash_files_for_prs (bool): When provided, all file metadata will be hashed for PRs
            limit (int, optional): When provided, the number of items returned is limited.
                Useful for the validation use case, where we want to just verify we can pull PRs.
                Defaults to None.

        Returns:
            List[StandardizedPullRequest]: A list of standardized PRs
        """
        raise NotImplementedError()
