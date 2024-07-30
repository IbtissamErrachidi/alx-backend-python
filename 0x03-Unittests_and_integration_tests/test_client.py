#!/usr/bin/env python3
"""
Test for GithubOrgClient class
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

GithubOrgClient = __import__('client').GithubOrgClient


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

class TestIntegrationGithubOrgClient(unittest.TestCase):
    """tests for the `GithubOrgClient` class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()


@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload, "expected_repos": expected_repos, "apache2_repos": apache2_repos},
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient class
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup the mock for requests.get
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Setup side_effects to return appropriate fixtures based on URL
        def side_effect(url):
            if url == 'https://api.github.com/orgs/test_org':
                return MockResponse(cls.org_payload)
            elif url == 'https://api.github.com/orgs/test_org/repos':
                return MockResponse(cls.repos_payload)
            else:
                return MockResponse({})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Stop the mock
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test the public_repos method with integration fixtures
        """
        client = GithubOrgClient('test_org')
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test the public_repos method with a specific license filter
        """
        client = GithubOrgClient('test_org')
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)

class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data
