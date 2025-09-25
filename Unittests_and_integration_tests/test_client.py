#!/usr/bin/env python3
"""Unit and Integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value
        
        Args:
            org_name: The organization name to test
            mock_get_json: Mocked get_json function
        """
        # Create test payload
        test_payload = {"name": org_name, "id": 12345}
        mock_get_json.return_value = test_payload
        
        # Create client and call org method
        client = GithubOrgClient(org_name)
        result = client.org
        
        # Assert the result is correct
        self.assertEqual(result, test_payload)
        
        # Assert get_json was called once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """Test the _public_repos_url property"""
        with patch('client.GithubOrgClient.org', 
                   new_callable=PropertyMock) as mock_org:
            # Set up the mock payload
            test_payload = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            mock_org.return_value = test_payload
            
            # Create client and access _public_repos_url
            client = GithubOrgClient("test")
            result = client._public_repos_url
            
            # Assert the result matches expected URL
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method"""
        # Set up test payload
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_repos_payload
        
        # Use patch as context manager for _public_repos_url
        with patch('client.GithubOrgClient._public_repos_url', 
                   new_callable=PropertyMock) as mock_public_repos_url:
            # Set the return value for _public_repos_url
            test_url = "https://api.github.com/orgs/test/repos"
            mock_public_repos_url.return_value = test_url
            
            # Create client and call public_repos
            client = GithubOrgClient("test")
            result = client.public_repos()
            
            # Expected repo names
            expected_repos = ["repo1", "repo2", "repo3"]
            
            # Assert the result matches expected
            self.assertEqual(result, expected_repos)
            
            # Assert _public_repos_url was called once
            mock_public_repos_url.assert_called_once()
            
            # Assert get_json was called once with the correct URL
            mock_get_json.assert_called_once_with(test_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license method
        
        Args:
            repo: Repository dictionary
            license_key: License key to check
            expected: Expected boolean result
        """
        client = GithubOrgClient("test")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""
    
    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before running tests"""
        # Configure the patcher for requests.get
        cls.get_patcher = patch('requests.get')
        
        # Start the patcher
        cls.mock_get = cls.get_patcher.start()
        
        # Configure side_effect to return appropriate fixtures
        def side_effect(url):
            """Side effect function for requests.get mock"""
            mock_response = Mock()
            if url.endswith("/orgs/google"):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith("/repos"):
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = None
            return mock_response
        
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Remove fixtures after running tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos method"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos method with license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
