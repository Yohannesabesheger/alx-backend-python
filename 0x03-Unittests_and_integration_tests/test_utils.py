#!/usr/bin/env python3
"""
Unit tests for the utils module.

This module includes parameterized and patched unit tests for:
- access_nested_map function
- get_json function
- memoize decorator

It uses unittest and parameterized testing techniques.
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the correct value
        for a valid path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that access_nested_map
        raises KeyError for invalid paths
        and the exception message matches the missing key.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        # Determine the expected missing key
        missing_key = (
            path[len(context.exception.args[0]):][0]
            if len(path) > 1 else path[0]
        )
        self.assertEqual(str(context.exception), repr(missing_key))


class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json function using mocking."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test that get_json returns the correct payload and that
        requests.get is called exactly once with the correct URL.
        """
        with patch("utils.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize decorator.

    This test ensures that methods decorated with @memoize
    cache their results and avoid redundant computations.
    """

    def test_memoize(self):
        """Test that a memoized method is 
        called only once and result is cached.
        """

        class TestClass:
            """
            This module contains the
            definition of the TestClass.

            Classes:
                TestClass: A sample class
                demonstrating the use of
                memoization and method/property definitions.

            Methods:
                a_method: Returns a constant value of 42.
                a_property: A memoized property
                that calls `a_method`
                and returns its result.
            """

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass, 'a_method', return_value=42
        ) as mock_method:
            obj = TestClass()

            # Call a_property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Assert correct result both times
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that a_method was called exactly once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
