import os
import sys
import json
import base64

import requests

github_auth = ('475c949a1d224108e2095d66f62c1d6c93095521', 'x-oauth-basic')
github_api_url = "https://api.github.com"

headers = {
    'accept': 'application/vnd.github.v3+json',
    'user-agent': 'https://github.com/SolsCo/challenge'
}

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

def delete_repo(owner, repo):
    print 'Delete {}/{}'.format(owner, repo)
    r = requests.delete('{}/repos/{}/{}'.format(github_api_url, owner, repo), auth=github_auth, headers=headers)
    r.raise_for_status()

def get_repo_name(candidate):
    return "challenge-{}".format(candidate.replace(' ', '-').lower())

def get_team_name(candidate):
    return 'Candidate: {}'.format(candidate)

def get_candidate_team(owner, candidate):
    r = requests.get('{}/repos/{}/{}/teams'.format(github_api_url, owner, get_repo_name(candidate)), auth=github_auth, headers=headers)
    r.raise_for_status()
    team = r.json()[0]
    if team['name'] != get_team_name(candidate):
        raise Exception('Candidate team not found')
    return team

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

def create_coding_challenge(username, team_usernames):
    user = get_user(username)
    candidate = user['name'] if 'name' in user else user['login']
    print 'Creating coding challenge for {}'.format(candidate)

    team = create_team(org='SolsCo',
                       name=get_team_name(candidate),
                       description='SOLS Coding Challenge for {}'.format(candidate),
                       repo_names=[],
                       permission='push')

    [add_team_membership(team['id'], u) for u in team_usernames]
    add_team_membership(team['id'], username)

    repo = create_repo(org='SolsCo',
                       name=get_repo_name(candidate),
                       description="SOLS Coding Challenge",
                       homepage='http://www.sols.co',
                       is_private=True,
                       has_issues=False,
                       has_wiki=False,
                       has_downloads=False,
                       team_id=team['id'],
                       auto_init=False,
                       gitignore_template=None,
                       license_template=None)

    add_file_to_repo(owner='SolsCo',
                     repo=repo['name'],
                     src_file='coding_challenge.md',
                     new_path='README.md',
                     commit_message='Coding challenge instructions')

def remove_coding_challenge(username):
    user = get_user(username)
    candidate = user['name']
    print 'Removing coding challenge for {}'.format(candidate) 
    team = get_candidate_team('SolsCo', candidate)
    delete_repo('SolsCo', get_repo_name(candidate))
    delete_team(team['id'])

def main(args):
    username = args.pop(0)
    if username == '--remove':
        username = args.pop(0)
        remove_coding_challenge(username)
    else:
        team_usernames = ['leslieb', 'jschementi', 'shyamvala', 'Cerennomer']
        create_coding_challenge(username, team_usernames)
    
if __name__ == '__main__':
    main(sys.argv[1:])
