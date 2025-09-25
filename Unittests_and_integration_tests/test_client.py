#!/usr/bin/env python3
"""
A module to test the client.py file.
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case for the GithubOrgClient class.
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value and that
        get_json is called once with the expected argument.
        """
        # Define a mock payload for get_json to return
        test_payload = {"login": org_name, "some_key": "some_value"}
        mock_get_json.return_value = test_payload

        # Create an instance of GithubOrgClient
        client = GithubOrgClient(org_name)

        # Call the method under test and assert its return value
        self.assertEqual(client.org(), test_payload)

        # Construct the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Assert that the mocked get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(expected_url)


if __name__ == '__main__':
    unittest.main()
