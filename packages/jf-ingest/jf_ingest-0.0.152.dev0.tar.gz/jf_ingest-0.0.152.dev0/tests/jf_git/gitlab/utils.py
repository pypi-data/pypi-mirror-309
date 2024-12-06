import json
from typing import Dict, List

import requests
import requests_mock

from jf_ingest.config import AzureDevopsAuthConfig, GitConfig, GitProvider
from jf_ingest.constants import Constants
from jf_ingest.jf_git.adapters.azure_devops import AzureDevopsAdapter
from jf_ingest.jf_git.standardized_models import (
    StandardizedOrganization,
    StandardizedRepository,
)

PATH_TO_TEST_FIXTURES = 'tests/jf_git/gitlab/fixtures'

TEST_COMPANY_SLUG = 'A-Company'
TEST_BASE_URL = 'https://www.a-website.com'
TEST_BASE_GQL_URL = f'{TEST_BASE_URL}/api/graphql'
TEST_TOKEN = 'A Spoofed Token'
TEST_ORG_LOGIN = '1'
TEST_FULL_PATH = 'test-full-path'
TEST_INSTANCE_SLUG = 'a-test-instance-slug'
TEST_INSTANCE_FILE_KEY = 'a-test-file-key'
EXPECTED_AUTH_HEADER = {
    'Authorization': f'Bearer {TEST_TOKEN}',
    'Content-Type': 'application/json',
    'User-Agent': f'{Constants.JELLYFISH_USER_AGENT} ({requests.utils.default_user_agent()})',
}

def get_fixture_data(file_name: str):
    with open(file=f'{PATH_TO_TEST_FIXTURES}/{file_name}', mode='r') as f:
        return json.loads(f.read())

def get_raw_organizations(page_number: int):
    return get_fixture_data(f'raw_organizations_page_{page_number}.json')

def spoof_organizations_through_gql(requests_mock: requests_mock.Mocker) -> List[Dict]:
    
    raw_group_data_page_1 = get_raw_organizations(page_number=1)
    raw_group_data_page_2 = get_raw_organizations(page_number=2)
    combined_raw_groups = []
    combined_raw_groups.extend(raw_group_data_page_1['data']['groupsQuery']['groups'])
    combined_raw_groups.extend(raw_group_data_page_2['data']['groupsQuery']['groups'])
    
    def _first_matcher(request: requests.Request):
        if 'after: null' in request.json()['query']:
            return True
        return None
    
    def _second_matcher(request: requests.Request):
        if 'after: "eyJuYW1lIjoi8J-QmCIsImlkIjoiODQ1NDE2MjYifQ"' in request.json()['query']:
            return True
        return None
    
    requests_mock.post(
        url=TEST_BASE_GQL_URL, 
        request_headers=EXPECTED_AUTH_HEADER,
        additional_matcher=_first_matcher,
        json=raw_group_data_page_1, 
    )
    
    requests_mock.post(
        url=TEST_BASE_GQL_URL,
        request_headers=EXPECTED_AUTH_HEADER,
        additional_matcher=_second_matcher,
        json=raw_group_data_page_2,
    )
    
    return combined_raw_groups