#!/usr/bin/env python3
"""
Test for access_nested_map function
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence) -> None:
    """
    Test the access_nested_map method raises an error when expected to
    """
    with self.assertRaises(Exception):
        access_nested_map(nested_map, path)
