#!/usr/bin/env python3
"""
A module to test the client.py file.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case for the GithubOrgClient class.
    """
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_payload, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value and that
        get_json is called once with the expected argument.
        """
        # Configure the mock to return the expected payload
        mock_get_json.return_value = expected_payload

        # Create an instance of GithubOrgClient
        client = GithubOrgClient(org_name)

        # Call the org property
        org_data = client.org

        # Construct the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Assert that get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(expected_url)

        # Assert that the result of client.org is the expected payload
        self.assertEqual(org_data, expected_payload)


if __name__ == '__main__':
    unittest.main()
