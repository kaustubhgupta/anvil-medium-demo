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

def getCleanedUserData(data: dict) -> dict:
    
    root = data['data']['user']
    cleanedData = {}
    cleanedData['name'] = root.get('name')
    cleanedData['totalCommits'] = int(root['contributionsCollection']['totalCommitContributions']) + int(root['contributionsCollection']['restrictedContributionsCount'])
    cleanedData['repositoriesContributedTo'] = root['repositoriesContributedTo']['totalCount']
    cleanedData['pullRequests'] = root['pullRequests']['totalCount']
    cleanedData['openIssues'] = root['openIssues']['totalCount']
    cleanedData['closedIssues'] = root['closedIssues']['totalCount']
    cleanedData['followers'] = root['followers']['totalCount']
    cleanedData['following'] = root['following']['totalCount']
    cleanedData['totalRepos'] = root['repositories']['totalCount']
    cleanedData['totalStars'] = sum([i['stargazers']['totalCount'] for i in root['repositories']['nodes']])
    cleanedData['photoURL'] = root['avatarUrl']
    cleanedData['profileBio'] = root['bio']
    cleanedData['location'] = root['location']
    cleanedData['twitterUsername'] = root['twitterUsername']

    return cleanedData
  
def getLanguageCounter(data: dict) -> dict:
    
    languageCounter = {}
    for i in data['data']['user']['repositories']['nodes']:
        langs = i['languages']['edges']
        if len(langs)!=0:
            for i in langs:
                if i['node']['name'] in languageCounter.keys():
                    languageCounter[i['node']['name']] += 1
                else:
                    languageCounter[i['node']['name']] = 1

    return languageCounter
  
@anvil.server.callable
def fetchStats(username: str) -> tuple:
    
    headers = {"Authorization": "bearer " + API_KEY}
    query_top_language = {
        "variables": {
          "username": username
        },
        "query": """
            query languageUsed($username: String!) {
            user(login: $username) {
              repositories(ownerAffiliations: OWNER, isFork: false, last: 100) {
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
    following {
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
    avatarUrl
    bio
    location
    twitterUsername
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
    
    print(r1.json(), r2.json())
    language_data = getLanguageCounter(r1.json())
    general_data = getCleanedUserData(r2.json())
    return (general_data, language_data)