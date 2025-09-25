#!/usr/bin/env python3
"""
A module for parameterizing a unit test and mocking HTTP calls.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """
    A class to test the access_nested_map function from the utils module.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the expected result.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that a KeyError is raised for the respective inputs.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    A class for testing the get_json function.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that utils.get_json returns the expected result.
        """
        # Create a mock response object and configure its json method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        
        # Configure the mock_get to return the mock_response
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_json(test_url)

        # Assert that the mocked get method was called exactly once with the correct URL
        mock_get.assert_called_once_with(test_url)

        # Assert that the output of get_json is equal to the test_payload
        self.assertEqual(result, test_payload)


if __name__ == '__main__':
    unittest.main()
