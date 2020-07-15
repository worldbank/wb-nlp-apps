import requests
import json

# Make sure to generate a token which can be acquired by:
# - Go to the Settings (navigate to the upper left menu) in your Github account
# - Click the Developer settings and choose Personal access tokens
# - Click Generate new token and make sure to set only the necessary access roles <READ ONLY PUBLIC REPOSITORIES>
# - Copy the generated token and dump into auth.json following the format below.
#     `headers = {"Authorization": "token <OAUTH-TOKEN>"}`
# - Make sure to add the auth.json to .gitignore to prevent leakage
with open('auth.json') as fl:
    headers = json.load(fl)


session = requests.Session()


def get_readme_objs():
    ### Enumerate all possible markups that can be used for a README file
    # https://github.com/github/markup/blob/master/README.md#markups
    readme_exts = [
        '', '.markdown', '.mdown', '.mkdn', '.md',
        '.textfile', '.rdoc', '.org', '.creole',
        '.mediawiki', '.wiki', '.rst',
        '.asciidoc', '.adoc', '.asc', '.pod'
    ]

    readmes = [f'README{ext}' for ext in readme_exts]
    readmes.extend([r.lower() for r in readmes])

    object_query = lambda x: '''
    readme''' + x['ix'] + ''':object(expression: "master:''' + x['readme'] + '''") {
      # id
      ... on Blob {
        text
      }
    }
    '''

    readme_objs = [object_query({'ix': str(ix), 'readme': readme}) for ix, readme in enumerate(readmes)]
    return readme_objs


### Implement and interface for the github GraphQL API
def gql_query(query):
    request = session.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code != 200:    
        return {
            'request': request,  # Useful to debug the problem
            'query': query
        }

    return request.json()


def gql_get_repo_readme(owner, name, readme_objs=None):
    if readme_objs is None:
        readme_objs = get_readme_objs()
        
    query = lambda objs_list: '''
    {
      repository(owner: "''' + owner + '''", name: "''' + name + '''") {
        repo_id: id
        description
        repo_updated_at: updatedAt
        repo_created_at: createdAt
        primary_language: primaryLanguage {
          name
        }
        homepage_url: homepageUrl
        license_info: licenseInfo {
          name
        }
        topics: repositoryTopics (first: 100) {
          edges {
            node {
              topic {
                name
              }
              url
            }
          }
        }
        stargazers {
          stars_count: totalCount
        }
        watchers {
          watchers_count: totalCount
        }
        fork_count: forkCount
        languages(first: 100) {
          edges {
            node {
              name
            }
          }
        }
        owner {
          id
        }''' + '\n'.join(objs_list) + '''
      }
      rateLimit {
        limit
        cost
        remaining
        resetAt
      }
    }
    '''
    
    return gql_query(query(readme_objs))
