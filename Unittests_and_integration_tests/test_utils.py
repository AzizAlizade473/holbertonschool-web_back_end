#!/usr/bin/env python3
"""
Unit tests for utils.memoize.
"""

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test class for the memoize decorator."""

    def test_memoize(self):
        """Test that a_method is only called once with @memoize."""

        class TestClass:
            """Test class with a method and a memoized property."""

            def a_method(self):
                """Return a fixed integer."""
                return 42

            @memoize
            def a_property(self):
                """Return the result of a_method, memoized."""
                return self.a_method()

        test_obj = TestClass()

        with patch.object(TestClass, "a_method",
                          return_value=42) as mock_method:
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
