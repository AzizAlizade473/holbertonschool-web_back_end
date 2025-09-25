#!/usr/bin/env python3
"""
A module for parameterizing a unit test, mocking HTTP calls, and testing memoization.
"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
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
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    A class for testing the memoize decorator.
    """
    def test_memoize(self):
        """
        Test that when calling a_property twice, the correct result is returned
        but a_method is only called once.
        """
        class TestClass:
            """A test class with a memoized property."""
            def a_method(self):
                """A method that returns a fixed value."""
                return 42

            @memoize
            def a_property(self):
                """A property that calls a_method and is memoized."""
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_a_method:
            test_instance = TestClass()
            
            # Call the memoized property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assert that the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that a_method was called only once
            mock_a_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
