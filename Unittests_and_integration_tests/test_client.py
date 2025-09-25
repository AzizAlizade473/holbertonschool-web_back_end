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
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org property returns the correct value.
        """
        # Define a test payload that the mock will return
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        # Create an instance of the client
        client = GithubOrgClient(org_name)

        # Access the 'org' property and assert its value
        self.assertEqual(client.org, test_payload)

        # Define the expected URL that should have been called
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Assert that the mocked get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns the correct URL
        based on the mocked payload of the 'org' property.
        """
        # Known payload for the 'org' property
        known_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        # Use patch.object as a context manager to mock the 'org' property
        with patch.object(GithubOrgClient,
                         'org',
                         new_callable=PropertyMock) as mock_org:
            # Configure the mock property to return the known payload
            mock_org.return_value = known_payload

            # Create an instance of GithubOrgClient
            client = GithubOrgClient("testorg")

            # Get the result from the _public_repos_url property
            result_url = client._public_repos_url

            # Assert that the result is the expected repos_url
            self.assertEqual(result_url, known_payload["repos_url"])


if __name__ == '__main__':
    unittest.main()
