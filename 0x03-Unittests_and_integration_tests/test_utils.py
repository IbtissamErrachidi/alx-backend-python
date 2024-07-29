#!/usr/bin/env python3
"""
Test for access_nested_map function
"""

import unittest
import requests
from unittest.mock import patch
from utils import access_nested_map, get_json, memoize
from typing import Mapping, Sequence, Any
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence) -> None:
    """
    Test the access_nested_map method raises an error when expected to
    """
    with self.assertRaises(Exception):
        access_nested_map(nested_map, path)
