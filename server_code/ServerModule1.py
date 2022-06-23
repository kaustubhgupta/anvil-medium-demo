import anvil.secrets
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import requests

s = requests.session()
API_KEY = anvil.secrets.get_secret('GITHUB_API_KEY')

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def fetchStats(username: str):
  headers = {"Authorization": "bearer " + API_KEY}
  query_top_language = {
    "variables": {
      "username": username
    },
    "query": """
        query languageUsed($username: String!) {
        user(login: $username) {
          repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
            nodes {
              languages(first: 50, orderBy: {field: SIZE, direction: DESC}) {
                edges {
                  node {
                    name
                  }
                }
              }
            }
          }
        }
      },
    """
  }
  
  query_general_info = {
    "variables": {
      "username": username
    },
    "query": """
      query userInfo($username: String!) {
      user(login: $username) {
        name
        login
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
        }
        repositoriesContributedTo(
          first: 1
          contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]
        ) {
          totalCount
        }
        pullRequests(first: 1) {
          totalCount
        }
        openIssues: issues(states: OPEN) {
          totalCount
        }
        closedIssues: issues(states: CLOSED) {
          totalCount
        }
        followers {
          totalCount
        }
        repositories(
          first: 100
          ownerAffiliations: OWNER
          orderBy: {direction: DESC, field: STARGAZERS}
        ) {
          totalCount
          nodes {
            stargazers {
              totalCount
            }
          }
        }
      }
    }
    """
  }
  r1 = s.post( 
           "https://api.github.com/graphql",
            json=query_top_language,
            headers=headers,
            timeout=15,
        )
  
  r2 = s.post( 
           "https://api.github.com/graphql",
            json=query_general_info,
            headers=headers,
            timeout=15,
        )
  language_data = r1.json()
  general_data = r2.json()
  return (general_data, language_data)