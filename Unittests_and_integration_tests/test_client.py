import unittest
from unittest.mock import patch
from utils import memoize # Assuming utils.py is in the same directory

class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_a_method:
            test_instance = TestClass()
            
            # First call to the memoized property
            result1 = test_instance.a_property
            self.assertEqual(result1, 42)
            
            # Second call to the same property
            result2 = test_instance.a_property
            self.assertEqual(result2, 42)

            # Assert that the mocked method was only called once
            mock_a_method.assert_called_once()
