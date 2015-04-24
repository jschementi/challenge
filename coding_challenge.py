import re
import sys

import github
github.set_user_agent('https://github.com/SolsCo/challenge')
github.set_oauth_token('475c949a1d224108e2095d66f62c1d6c93095521')

org = 'SolsCo'
coding_challenge_description = 'SOLS Coding Challenge for {candidate}'
repo_homepage = 'http://www.sols.co'

teams = ['engineers', 'recruiting']

team_ids = [github.get_team(org, t)['id'] for t in teams]

def get_repo_name(candidate):
    return "challenge-{}".format(candidate.replace(' ', '-').lower())

def get_team_name(candidate):
    return 'Candidate: {}'.format(candidate)

def list_coding_challenges():
    return [repo for repo in github.list_repos(org=org) if re.match('^challenge-', repo['name'], re.I)]

def search_users(q):
    return github.search_users(q)

def create_coding_challenge(username):
    user = github.get_user(username)
    candidate = user['name'] if 'name' in user else user['login']

    print 'Creating coding challenge for {}'.format(candidate)

    team = github.create_team(org=org,
                              name=get_team_name(candidate),
                              description=coding_challenge_description.format(candidate=candidate),
                              repo_names=[],
                              permission='push')

    github.add_team_membership(team['id'], username)

    repo_name = get_repo_name(candidate)
    repo = github.create_repo(org=org,
                              name=repo_name,
                              description=coding_challenge_description.format(candidate=candidate),
                              homepage=repo_homepage,
                              is_private=True,
                              has_issues=False,
                              has_wiki=False,
                              has_downloads=False,
                              team_id=team['id'],
                              auto_init=False,
                              gitignore_template=None,
                              license_template=None)

    github.add_file_to_repo(owner=org,
                            repo=repo['name'],
                            src_file='coding_challenge.md',
                            new_path='README.md',
                            commit_message='Coding challenge instructions')

    for team_id in team_ids:
        github.add_team_repository(team_id, org, repo_name)

    return candidate, team, repo

def remove_coding_challenge(username):
    user = github.get_user(username)
    candidate = user['name']
    print 'Removing coding challenge for {}'.format(candidate) 
    team = github.get_repo_team(org, get_repo_name(candidate), get_team_name(candidate))
    github.delete_repo(org, get_repo_name(candidate))
    github.delete_team(team['id'])

def main(args):
    username = args.pop(0)
    if username == '--remove':
        username = args.pop(0)
        remove_coding_challenge(username)
    else:
        create_coding_challenge(username)
    
if __name__ == '__main__':
    main(sys.argv[1:])
