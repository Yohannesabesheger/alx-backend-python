#!/usr/bin/env python3
"""
Unit tests for the client module.

This module tests the GithubOrgClient class using parameterized
inputs and patching external calls.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from utils import get_json
from unittest.mock import patch, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct payload
        and calls get_json with the right URL.
        """
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

        def test_public_repos_url(self):
            """
        Test that GithubOrgClient._public_repos_url returns the
        correct URL from the mocked org payload.
        """
        expected_url = "https://api.github.com/orgs/testorg/repos"
        payload = {"repos_url": expected_url}

        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("testorg")

            result = client._public_repos_url
            self.assertEqual(result, expected_url)


if __name__ == "__main__":
    unittest.main()
