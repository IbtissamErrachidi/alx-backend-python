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
         """Tests the `_public_repos_url` property."""
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        client = GithubOrgClient("test_org")

        expected_url = "https://api.github.com/orgs/test_org/repos"
        self.assertEqual(client._public_repos_url, expected_url)

     @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the correct list of repos.
        """
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        
        with patch.object(GithubOrgClient, '_public_repos_url', return_value='https://api.github.com/orgs/test_org/repos'):
            client = GithubOrgClient("test_org")
            result = client.public_repos()
            expected_result = ["repo1", "repo2"]
            self.assertEqual(result, expected_result)

            mock_get_json.assert_called_once_with('https://api.github.com/orgs/test_org/repos')

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test  GithubOrgClient.has_license .
        """
        with patch.object(GithubOrgClient, 'org', return_value=repo):
            client = GithubOrgClient("test_org")
            result = client.has_license(license_key)
            self.assertEqual(result, expected)
