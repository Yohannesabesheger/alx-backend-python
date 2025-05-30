# client.py

import requests

class GithubOrgClient:
    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        self.org_name = org_name

    def org(self):
        """Fetch organization info from GitHub"""
        url = self.ORG_URL.format(self.org_name)
        return requests.get(url).json()

    def public_repos_url(self):
        """Get public repos URL from org data"""
        return self.org().get("repos_url")

    def public_repos(self):
        """List the names of public repositories"""
        repos_url = self.public_repos_url()
        response = requests.get(repos_url)
        return [repo['name'] for repo in response.json()]
