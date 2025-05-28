#!/usr/bin/env python3
import unittest
from nose.tools import assert_equal
from parameterized import parameterized, parameterized_class
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Unit test class for access_nested_map"""

    @parameterized.expand([
    ({"a": 1}, ("a",), 1),  # Corrected expected result
])

    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)
