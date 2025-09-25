#!/usr/bin/env python3
"""Unit tests for utils module"""

import unittest
from unittest.mock import patch, Mock
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test class for memoize decorator"""

    def test_memoize(self):
        """Test that memoize decorator works correctly"""
        
        class TestClass:
            """Test class to demonstrate memoize"""
            
            def a_method(self):
                """A method that returns 42"""
                return 42
            
            @memoize
            def a_property(self):
                """A memoized property that calls a_method"""
                return self.a_method()
        
        # Create instance and patch a_method
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            test_instance = TestClass()
            
            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property
            
            # Assert both calls return the same result
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            
            # Assert a_method was only called once (memoization works)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
