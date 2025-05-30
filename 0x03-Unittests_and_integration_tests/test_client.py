#!/usr/bin/env python3
"""
Integration tests for GithubOrgClient using parameterized fixtures.

Mocks external HTTP requests but tests the integration of
public_repos method with realistic payloads.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for GithubOrgClient.
    Mocks external requests.get but uses real client methods.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the patcher for requests.get to mock GitHub API responses
        based on URL and provide fixture data.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            mock_response = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload['repos_url']:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = None
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test that public_repos method returns expected repository names.
        """
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test filtering of repos by license using the apache2_repos fixture.
        """
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
