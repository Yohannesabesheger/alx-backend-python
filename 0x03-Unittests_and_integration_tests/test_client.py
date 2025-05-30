#!/usr/bin/env python3
"""
Unit tests for the client module.

This module tests the GithubOrgClient class using parameterized
inputs and patching external calls.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient
import fixtures
from utils import get_json

from parameterized import parameterized_class

@parameterized_class([
    {
        'org_payload': fixtures.org_payload,
        'repos_payload': fixtures.repos_payload,
        'expected_repos': fixtures.expected_repos,
        'apache2_repos': fixtures.apache2_repos
    }
])


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.

    Tests include:
    - org property returns expected payload and calls get_json once.
    - _public_repos_url returns correct repos URL from mocked org payload.
    - public_repos returns list of repo names from mocked API responses.
    - has_license correctly verifies if a repo has a given license key.
    """

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct payload
        and calls get_json with the expected URL once.
        """
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns the
        correct repos URL from the mocked org payload.
        """
        expected_url = "https://api.github.com/orgs/testorg/repos"
        payload = {"repos_url": expected_url}

        with patch.object(
                GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("testorg")

            result = client._public_repos_url
            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns a list of
        repository names, and that dependencies are called once.
        """
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        test_url = "https://api.github.com/orgs/testorg/repos"

        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = test_url

            client = GithubOrgClient("testorg")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(test_url)
            mock_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test the has_license method of GithubOrgClient.
        """
        self.assertEqual(GithubOrgClient.has_license(
            repo, license_key), expected)
    @classmethod
    def setUpClass(cls):
        """Patch requests.get for the duration of all tests in the class"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Define side effects of successive calls to requests.get
        cls.mock_get.side_effect = [
            fixtures.org_payload,  # First call: .org()
            fixtures.repos_payload  # Second call: .public_repos()
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method returns expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license='apache-2.0'"""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)

if __name__ == "__main__":
    unittest.main()
