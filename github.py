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

def remove_team_membership(team_id, username):
    print 'Removing {} from team {}'.format(username, team_id)
    r = requests.delete('{}/teams/{}/memberships/{}'.format(github_api_url, team_id, username), auth=github_auth, headers=headers)
    r.raise_for_status()

def add_team_repository(team_id, org, repo):
    print 'Add team {} to {}/{}'.format(team_id, org, repo)
    r = requests.put('{}/teams/{}/repos/{}/{}'.format(github_api_url, team_id, org, repo), auth=github_auth, headers=headers)
    r.raise_for_status()

def list_teams(org):
    print 'Getting {} teams'.format(org)
    return requests_paged_as_json('get', '{}/orgs/{}/teams'.format(github_api_url, org), auth=github_auth, headers=headers)

def get_team(org, team_value, by="slug"):
    print 'Get {} teams where {}={}'.format(org, by, team_value)
    teams = list_teams(org)
    eng_team = [team for team in teams if team[by] == team_value]
    if len(eng_team) == 1:
        return eng_team[0]

def get_repo(org, name):
    print 'Get {}/{}'.format(org, name)
    r = requests.get('{}/repos/{}/{}'.format(github_api_url, org, name), auth=github_auth, headers=headers)
    response_json = r.json()
    if r.ok:
        return response_json
    elif 'message' in response_json and response_json['message'] == 'Not Found':
        return None
    else:
        r.raise_for_status()

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

def create_pull_request(repo, title, head, base, body):
    print 'Creating pull request for {}'.format(repo)
    r = requests.post('{}/repos/{}/{}/pulls'.format(github_api_url, org, repo),
        auth=github_auth,
        headers=headers,
        title=title,
        head=head,
        base=base,
        body=body)
    r.raise_for_status()

def list_repos(org, repo_type='all'):
    print 'Listing repos in {}'.format(org)
    return requests_paged_as_json('get',
                                  '{}/orgs/{}/repos?type={}'.format(github_api_url, org, repo_type),
                                  auth=github_auth, headers=headers)

def delete_repo(owner, repo):
    print 'Delete {}/{}'.format(owner, repo)
    r = requests.delete('{}/repos/{}/{}'.format(github_api_url, owner, repo), auth=github_auth, headers=headers)
    r.raise_for_status()

def remove_collaborator_from_repo(owner, user, repo):
    print 'Delete user {} from {}'.format(owner, repo)
    r = requests.delete('{}/repos/{}/{}/collaborators/{}'.format(github_api_url, owner, repo, user), auth=github_auth, headers=headers)
    r.raise_for_status()

def get_repo_team(owner, repo, team):
    print 'Get team {} in {}/{}'.format(team, owner, repo)
    r = requests.get('{}/repos/{}/{}/teams'.format(github_api_url, owner, repo), auth=github_auth, headers=headers)
    r.raise_for_status()
    t = r.json()[0]
    if t['name'] != team:
        return None
    return t

def get_user(username):
    print 'Get user {}'.format(username)
    r = requests.get('{}/users/{}'.format(github_api_url, username), auth=github_auth, headers=headers)
    r.raise_for_status()
    return r.json()

def get_file_contents_from_repo(owner, repo, path):
    print 'Get file contents for {}/{}/{}'.format(owner, repo, path)
    r = requests.get('{}/repos/{}/{}/contents/{}'.format(github_api_url, owner, repo, path), auth=github_auth, headers=headers)
    return {'body': r.json(), 'ok': r.ok}

def update_file_contents(owner, repo, version, src_file, path, commit_message):
    print 'Update {}/{}/{} with contents of {}: {}'.format(owner, repo, path, src_file, commit_message)
    with open(src_file) as f:
        r = requests.put('{}/repos/{}/{}/contents/{}'.format(github_api_url, owner, repo, path),
                         data=json.dumps({'message': commit_message,
                                          'content': base64.b64encode(f.read()),
                                          'sha': version
                                         }),
                         auth=github_auth,
                         headers=headers)
    r.raise_for_status()
    return r.json()

def update_file_contents_if_different(owner, repo, src_file, path, commit_message):
    print 'Checking to see if {} and {} are different'.format(src_file, path)
    result = get_file_contents_from_repo(owner, repo, path)
    if not result['ok']:
        return None
    with open(src_file) as f:
        data = f.read()
        if base64.b64decode(result['body']['content']) != data:
            print "Different! Updating..."
            update_file_contents(owner, repo, version, src_file, path, commit_message)
        else:
            print "Same! Nothing to do..."

def add_file_to_repo(owner, repo, src_file, new_path, commit_message):
    print 'Add {}/{}/{} with contents of {}: {}'.format(owner, repo, new_path, src_file, commit_message)
    with open(src_file) as f:
        r = requests.put('{}/repos/{}/{}/contents/{}'.format(github_api_url, owner, repo, new_path), data=json.dumps({
                             'message': commit_message,
                             'content': base64.b64encode(f.read())
                          }), auth=github_auth, headers=headers)
        r.raise_for_status()

def ensure_file_contents(owner, repo, src_file, path, new_commit_message, update_commit_message):
    print 'Ensure contents of {} is same as {}/{}/{}'.format(src_file, owner, repo, path)
    result = get_file_contents_from_repo(owner, repo, path)
    if result['ok']:
        update_file_contents_if_different(owner, repo, src_file, path, update_commit_message)
    else:
        add_file_to_repo(owner, repo, src_file, path, new_commit_message)

def search_users(q):
    print "Searching for user: {}".format(q)
    r = requests.get('{}/search/users'.format(github_api_url),
                     params={'q': q},
                     auth=github_auth, headers=headers)
    r.raise_for_status()
    return r.json()['items']

def get_team_membership(team_id, username):
    print 'Getting team {} membership for {}'.format(team_id, username)
    r = requests.get('{}/teams/{}/memberships/{}'.format(github_api_url, team_id, username), auth=github_auth, headers=headers)
    return r.json(), r.status_code

def get_org_membership(org, username):
    print 'Getting org {} membership for {}'.format(org, username)
    r = requests.get('{}/orgs/{}/members/{}'.format(github_api_url, org, username), auth=github_auth, headers=headers)
    return r.status_code
