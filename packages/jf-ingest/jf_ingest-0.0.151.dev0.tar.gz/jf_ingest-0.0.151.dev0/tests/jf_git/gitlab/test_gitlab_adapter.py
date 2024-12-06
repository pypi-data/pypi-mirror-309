import pytest
import requests_mock
from jf_ingest.config import GitAuthConfig, GitConfig, GitProvider
from jf_ingest.jf_git.adapters import GitAdapter
from jf_ingest.jf_git.adapters.gitlab import GitlabAdapter
from jf_ingest.jf_git.clients.gitlab import GitlabClient
from jf_ingest.jf_git.standardized_models import StandardizedOrganization
from tests.jf_git.gitlab.utils import EXPECTED_AUTH_HEADER, TEST_BASE_URL, TEST_COMPANY_SLUG, TEST_INSTANCE_FILE_KEY, TEST_INSTANCE_SLUG, TEST_TOKEN, spoof_organizations_through_gql

TEST_GIT_AUTH_CONFIG = GitAuthConfig(
        company_slug=TEST_COMPANY_SLUG,
        base_url=TEST_BASE_URL,
        token=TEST_TOKEN,
        verify=False,
    )

GITLAB_GIT_CONFIG = GitConfig(
    company_slug=TEST_COMPANY_SLUG,
    instance_slug=TEST_INSTANCE_SLUG,
    instance_file_key=TEST_INSTANCE_FILE_KEY,
    git_provider=GitProvider.GITLAB,
    git_auth_config=TEST_GIT_AUTH_CONFIG
)

def _get_gitlab_adapter() -> GitlabAdapter:
    return GitAdapter.get_git_adapter(GITLAB_GIT_CONFIG)

def test_gitlab_adapter():
    gitlab_adapter = _get_gitlab_adapter()
    assert type(gitlab_adapter) == GitlabAdapter
    assert gitlab_adapter.config.git_provider == GitProvider.GITLAB
    assert type(gitlab_adapter.client) == GitlabClient
    
@pytest.fixture
def gitlab_adapter():
    return _get_gitlab_adapter()
    
def test_gitlab_adapter_supports_date_filtering(gitlab_adapter: GitlabAdapter):
    assert gitlab_adapter.git_provider_pr_endpoint_supports_date_filtering() == True
    
def test_gitlab_adapter_get_api_scopes(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_api_scopes()
        
def test_gitlab_adapter_get_group_id_from_gid():
    group_id = '1234'
    gid = f'gid://gitlab/Group/{group_id}'
    assert GitlabAdapter._get_group_id_from_gid(gid) == group_id
    
    group_id = 'applecatbanana'
    gid = f'gid://gitlab/Group/{group_id}'
    assert GitlabAdapter._get_group_id_from_gid(gid) == group_id
        
def test_gitlab_adapter_get_new_organizations_with_gql(gitlab_adapter: GitlabAdapter, requests_mock: requests_mock.Mocker):
    raw_groups = spoof_organizations_through_gql(requests_mock)
    gitlab_adapter.config.discover_organizations = True
    standardized_organizations = gitlab_adapter.get_organizations()
    
    assert len(raw_groups) == len(standardized_organizations)
    for standardized_org, raw_group in zip(standardized_organizations, raw_groups):
        assert type(standardized_org) == StandardizedOrganization
        group_id = gitlab_adapter._get_group_id_from_gid(raw_group['id'])
        assert standardized_org.id == group_id
        assert standardized_org.login == group_id
        assert standardized_org.name == raw_group['name']
        assert standardized_org.url == raw_group['webUrl']
        # Assert that we are staching a mapping between group ID and full path
        assert group_id in gitlab_adapter.group_id_to_full_path
        assert gitlab_adapter.get_group_full_path_from_id(group_id=group_id) == raw_group['fullPath']

        
def test_gitlab_adapter_get_no_new_organizations_using_rest(gitlab_adapter: GitlabAdapter, requests_mock: requests_mock.Mocker):
    gitlab_adapter.config.discover_organizations = False
    group_ids_to_get = ['1', '2', '3']
    gitlab_adapter.config.git_organizations = group_ids_to_get
    
    def _construct_fake_name(id: str):
        return f'name-{id}'
    
    def _construct_fake_web_url(id: str):
        return f'www.website.com/{id}'
    
    for id in group_ids_to_get:
        requests_mock.get(
            url=f'{TEST_BASE_URL}/api/v4/groups/{id}?with_projects=False',
            headers=EXPECTED_AUTH_HEADER,
            json={
                'id': f'gid://gitlab/Group/{id}',
                'name': _construct_fake_name(id),
                'full_path': f'full_path_for_{id}',
                'web_url': _construct_fake_web_url(id)
            }
        )
    
    standardized_organizations = gitlab_adapter.get_organizations()
    
    assert len(group_ids_to_get) == len(standardized_organizations)
    for standardized_org, group_id in zip(standardized_organizations, group_ids_to_get):
        assert standardized_org.id == group_id
        assert standardized_org.login == group_id
        assert standardized_org.name == _construct_fake_name(group_id)
        assert standardized_org.url == _construct_fake_web_url(group_id)
        # assert we are caching group ID to group full path
        assert group_id in gitlab_adapter.group_id_to_full_path
        assert f'full_path_for_{group_id}' == gitlab_adapter.get_group_full_path_from_id(group_id)
        
def test_gitlab_adapter_get_group_full_path_from_id(gitlab_adapter: GitlabAdapter, requests_mock: requests_mock.Mocker):
    gitlab_adapter.config.discover_organizations = False
    group_ids_to_get = ['1', '2', '3']
    gitlab_adapter.config.git_organizations = group_ids_to_get
    
    def _construct_fake_name(id: str):
        return f'name-{id}'
    
    def _construct_fake_web_url(id: str):
        return f'www.website.com/{id}'
    
    for id in group_ids_to_get:
        requests_mock.get(
            url=f'{TEST_BASE_URL}/api/v4/groups/{id}?with_projects=False',
            headers=EXPECTED_AUTH_HEADER,
            json={
                'id': f'gid://gitlab/Group/{id}',
                'name': _construct_fake_name(id),
                'full_path': f'full_path_for_{id}',
                'web_url': _construct_fake_web_url(id)
            }
        )
        
    for group_id in group_ids_to_get:
        # Assert when we don't have group ID cached that we will get it and then cache it
        assert group_id not in gitlab_adapter.group_id_to_full_path
        assert f'full_path_for_{group_id}' == gitlab_adapter.get_group_full_path_from_id(group_id)
        assert group_id in gitlab_adapter.group_id_to_full_path
        

def test_gitlab_adapter_get_group_full_path_from_id_assert_caching(gitlab_adapter: GitlabAdapter):
    group_id_to_full_pathes = {
        '1': 'full_path_1',
        '2': 'full_path_2',
        '3': 'full_path_3'
    }
    
    gitlab_adapter.group_id_to_full_path = group_id_to_full_pathes
    
    for group_id, full_path in group_id_to_full_pathes.items():
        # Assert we are using the dictionary and never making an API call
        assert gitlab_adapter.get_group_full_path_from_id(group_id) == full_path
    
    
def test_gitlab_get_users(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_users(standardized_organization=None)
        
def test_gitlab_get_teams(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_teams(
            standardized_organization=None
        )
        
def test_gitlab_get_repos(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_repos(
            standardized_organization=None
        )
        
def test_gitlab_get_commits_for_default_branch(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_commits_for_default_branch(
            standardized_repo=None
        )
        
def test_gitlab_get_branches_for_repo(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_branches_for_repo(
            standardized_repo=None
        )
        
def test_gitlab_get_commits_for_branches(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_commits_for_branches(
            standardized_repo=None,
            branches=[]
        )
        
def test_gitlab_get_pr_metadata(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_pr_metadata(
            standardized_repo=None,
        )
        
def test_gitlab_get_prs(gitlab_adapter: GitlabAdapter):
    with pytest.raises(NotImplementedError):
        gitlab_adapter.get_prs(
            standardized_repo=None,
        )
    