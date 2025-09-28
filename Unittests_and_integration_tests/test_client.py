#!/usr/bin/env python3
"""
Unit tests and integration tests for client.GithubOrgClient
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import (org_payload, repos_payload, expected_repos,
                      apache2_repos, TEST_PAYLOAD)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client_obj = GithubOrgClient(org_name)
        result = client_obj.org

        mock_get_json.assert_called_once()
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected URL"""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload

            client_obj = GithubOrgClient("google")
            result = client_obj._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repos"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos"
            )

            client_obj = GithubOrgClient("google")
            result = client_obj.public_repos()

            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license with different license keys"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


# ---------------- Integration Tests ---------------- #

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
        "TEST_PAYLOAD": TEST_PAYLOAD,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide mocks before tests"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def mock_json(url):
            if url.endswith("/orgs/google"):
                return cls.org_payload
            if url.endswith("/orgs/google/repos"):
                return cls.repos_payload
            return None

        mock_get.return_value.json.side_effect = mock_json

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos"""
        client_obj = GithubOrgClient("google")
        repos = client_obj.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license filtering"""
        client_obj = GithubOrgClient("google")
        repos = client_obj.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
