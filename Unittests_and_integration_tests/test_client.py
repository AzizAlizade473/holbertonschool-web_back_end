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
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns the correct URL
        based on the mocked payload of the 'org' property.
        """
        known_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }
        with patch.object(GithubOrgClient,
                         'org',
                         new_callable=PropertyMock) as mock_org:
            mock_org.return_value = known_payload
            client = GithubOrgClient("testorg")
            result_url = client._public_repos_url
            self.assertEqual(result_url, known_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test the public_repos property of GithubOrgClient.
        It should return the list of repository names based on the payload
        from the mocked get_json and _public_repos_url.
        """
        # Define the payload that get_json will return for the repos endpoint
        json_payload = [
            {"name": "repo-one"},
            {"name": "repo-two"},
            {"name": "repo-three"}
        ]
        mock_get_json.return_value = json_payload

        # Mock the _public_repos_url property using a context manager
        with patch.object(GithubOrgClient,
                         '_public_repos_url',
                         new_callable=PropertyMock) as mock_public_repos_url:
            # Set a known return value for the mocked property
            repos_url = "https://api.github.com/orgs/test/repos"
            mock_public_repos_url.return_value = repos_url

            # Create an instance and access the property under test
            client = GithubOrgClient("test")
            repos = client.public_repos  # Access as a property

            # Assert that the list of repos is what we expect
            expected_repos = ["repo-one", "repo-two", "repo-three"]
            self.assertEqual(repos, expected_repos)

            # Assert that the mocked property was called once
            mock_public_repos_url.assert_called_once()

            # Assert that get_json was called once with the correct URL
            mock_get_json.assert_called_once_with(repos_url)


if __name__ == '__main__':
    unittest.main()
