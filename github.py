import base64
import json
import os

import requests

github_auth = (None, 'x-oauth-basic')
github_api_url = "https://api.github.com"
headers = {
    'accept': 'application/vnd.github.v3+json'
}

def requests_paged_as_json(method, url, *args, **kwargs):
    data = []
    current_url = url
    while True:
        r = getattr(requests, method)(current_url, *args, **kwargs)
        r.raise_for_status()
        data.extend(r.json())
        if not ('next' in r.links):
            break
        current_url = r.links['next']['url']
    return data

def set_user_agent(ua):
    headers['user-agent'] = ua

def set_oauth_token(token):
    global github_auth
    github_auth = (token, github_auth[1])

def get_repo_path(repo_url):
    return os.path.splitext(repo_url)[0].split('github.com')[1][1:].split('/')

def create_team(org, name, description, repo_names, permission):
    print 'Create team "{}" in {}'.format(name, org)
    r = requests.post('{}/orgs/{}/teams'.format(github_api_url, org), data=json.dumps({
            'name': name,
            'description': description,
            'repo_names': repo_names,
            'permission': permission
        }), auth=github_auth, headers=headers)
    r.raise_for_status()
    return r.json()

def delete_team(team_id):
    print 'Delete team {}'.format(team_id)
    r = requests.delete('{}/teams/{}'.format(github_api_url, team_id), auth=github_auth, headers=headers)
    r.raise_for_status()

def add_team_membership(team_id, username):
    print 'Add {} to team {}'.format(username, team_id)
    r = requests.put('{}/teams/{}/memberships/{}'.format(github_api_url, team_id, username), auth=github_auth, headers=headers)
    r.raise_for_status()
    return r.json()

def add_team_repository(team_id, org, repo):
    r = requests.put('{}/teams/{}/repos/{}/{}'.format(github_api_url, team_id, org, repo), auth=github_auth, headers=headers)
    r.raise_for_status()

def list_teams(org):
    return requests_paged_as_json('get', '{}/orgs/{}/teams'.format(github_api_url, org), auth=github_auth, headers=headers)

def get_team(org, team_slug):
    teams = list_teams(org)
    eng_team = [team for team in teams if team['slug'] == team_slug]
    if len(eng_team) == 1:
        return eng_team[0]

def create_repo(org, name, description, homepage, is_private, has_issues, has_wiki, has_downloads, team_id, auto_init, gitignore_template, license_template):
    print 'Create repo "{}/{}"'.format(org, name)
    r = requests.post('{}/orgs/{}/repos'.format(github_api_url, org), data=json.dumps({
            'name': name,
            'description': description,
            'homepage': homepage,
            'private': is_private,
            'has_issues': has_issues,
            'has_wiki': has_wiki,
            'has_downloads': has_downloads,
            'team_id': team_id,
            'auto_init': auto_init,
            'gitignore_template': gitignore_template,
            'license_template': license_template
        }), auth=github_auth, headers=headers)
    r.raise_for_status()
    return r.json()

def list_repos(org, repo_type='all'):
    print 'Listing repos in {}'.format(org)
    return requests_paged_as_json('get',
                                  '{}/orgs/{}/repos?type={}'.format(github_api_url, org, repo_type),
                                  auth=github_auth, headers=headers)

def delete_repo(owner, repo):
    print 'Delete {}/{}'.format(owner, repo)
    r = requests.delete('{}/repos/{}/{}'.format(github_api_url, owner, repo), auth=github_auth, headers=headers)
    r.raise_for_status()

def get_repo_team(owner, repo, team):
    r = requests.get('{}/repos/{}/{}/teams'.format(github_api_url, owner, repo), auth=github_auth, headers=headers)
    r.raise_for_status()
    t = r.json()[0]
    if t['name'] != team:
        raise Exception('Candidate team not found')
    return t

def get_user(username):
    r = requests.get('{}/users/{}'.format(github_api_url, username), auth=github_auth, headers=headers)
    r.raise_for_status()
    return r.json()

def add_file_to_repo(owner, repo, src_file, new_path, commit_message):
    print 'Add {} to {}/{} as {}'.format(src_file, owner, repo, new_path)
    with open(src_file) as f:
        r = requests.put('{}/repos/{}/{}/contents/{}'.format(github_api_url, owner, repo, new_path), data=json.dumps({
                             'message': commit_message,
                             'content': base64.b64encode(f.read())
                          }), auth=github_auth, headers=headers)
        r.raise_for_status()

def search_users(q):
    r = requests.get('{}/search/users'.format(github_api_url),
                     params={'q': q},
                     auth=github_auth, headers=headers)
    r.raise_for_status()
    return r.json()['items']

def get_team_membership(team_id, username):
    r = requests.get('{}/teams/{}/memberships/{}'.format(github_api_url, team_id, username), auth=github_auth, headers=headers)
    return r.json(), r.status_code

