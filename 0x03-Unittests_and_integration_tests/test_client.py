#!/usr/bin/env python3
"""
Test for GithubOrgClient class
"""

import unittest
from unittest.mock import patch
from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for GithubOrgClient class
    """

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch('client.GithubOrgClient.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        """

        mock_get_json.return_value = {"org": org_name}

        client = GithubOrgClient(org_name)

        result = client.org
        self.assertEqual(result, {"org": org_name})

        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{org_name}')

    @patch.object(GithubOrgClient, 'org', new_callable=property)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the expected URL based on the mocked org property.
        """

        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        client = GithubOrgClient("test_org")

        expected_url = "https://api.github.com/orgs/test_org/repos"
        self.assertEqual(client._public_repos_url, expected_url)
