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
        # Define the mock return value for get_json
        mock_get_json.return_value = {"org": org_name}

        # Create an instance of GithubOrgClient with the test org name
        client = GithubOrgClient(org_name)

        # Call the org method and verify the return value
        result = client.org
        self.assertEqual(result, {"org": org_name})

        # Verify that get_json was called once with the expected argument
        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{org_name}')
