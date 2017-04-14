from __future__ import print_function

import re
import sys
import traceback

# START dotenv
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# END dotenv

import github
github.set_user_agent('https://github.com/jschementi/challenge')
github.set_oauth_token(os.getenv("GITHUB_TOKEN"))

org = os.getenv("GITHUB_ORG")
org_admin = os.getenv("GITHUB_ADMIN")
coding_challenge_description = 'Coding Challenge for {username}'
repo_homepage = os.getenv("HOMEPAGE")

teams = [os.getenv("GITHUB_ENGINEERING_TEAM"), os.getenv("GITHUB_RECRUITING_TEAM")]

team_ids = [github.get_team(org, t)['id'] for t in teams]

def get_repo_name(username):
    return "challenge-{}".format(username)

def get_team_name(username):
    return 'Candidate: {}'.format(username)

def list_coding_challenges():
    return [repo for repo in github.list_repos(org=org) if re.match('^challenge-', repo['name'], re.I)]

def search_users(q):
    return github.search_users(q)

def get_username(user):
    return user['login']

def create_coding_challenge(username):
    user = github.get_user(username)
    username = get_username(user)

    print('Creating coding challenge for {}'.format(username))
    team_name = get_team_name(username)

    team = github.get_team(org, team_name, by='name')
    if not team:
        team = github.create_team(org=org,
                                  name=team_name,
                                  description=coding_challenge_description.format(username=username),
                                  repo_names=[],
                                  permission='push')

    github.add_team_membership(team['id'], username)

    repo_name = get_repo_name(username)
    repo = github.get_repo(org, repo_name)
    if not repo:
        repo = github.create_repo(org=org,
                                  name=repo_name,
                                  description=coding_challenge_description.format(username=username),
                                  homepage=repo_homepage,
                                  is_private=True,
                                  has_issues=False,
                                  has_wiki=False,
                                  has_downloads=False,
                                  team_id=team['id'],
                                  auto_init=False,
                                  gitignore_template=None,
                                  license_template=None)

    github.ensure_file_contents(owner=org,
                                repo=repo['name'],
                                src_file='coding_challenge.md',
                                path='README.md',
                                new_commit_message='Coding challenge instructions',
                                update_commit_message='Update coding challenge instructions')

    for team_id in team_ids:
        github.add_team_repository(team_id, org, repo_name)

    return username, team, repo

def remove_coding_challenge(username):
    user = github.get_user(username)
    username = get_username(user)
    print('Removing coding challenge for {}'.format(username))
    team = github.get_repo_team(org, get_repo_name(username), get_team_name(username))
    first_error = None
    try:
        github.delete_repo(org, get_repo_name(username))
    except Exception as e:
        if first_error is None:
            first_error = e
        print_exception(e)
    try:
        if team is not None:
            github.delete_team(team['id'])
    except Exception as e:
        if first_error is None:
            first_error = e
        print_exception(e)
    if first_error:
        raise first_error

def remove_user_from_repo(username):
    """
    Candidate is added to a team, then team is added to repo. Simplest way is to delete their team
    """
    user = github.get_user(username)
    username = get_username(user)
    team = github.get_team(org, get_team_name(username), by='name')
    print('Removing {} from repo {}'.format(username, get_repo_name(username)))
    first_error = None
    try:
        github.delete_team(team['id'])
    except Exception as e:
        if first_error is None:
            first_error = e
        print_exception(e)
    if first_error:
        raise first_error

def is_candidate_in_review(username):
    team_name = get_team_name(username)
    repo = get_repo_name(username)
    try:
        team = github.get_repo_team(org, repo, team_name)
        return team is None
    except Exception as e:
        return False

def get_last_update(username):
    repo = get_repo_name(username)
    try:
        commits = github.list_commits_on_repo(org, repo, username)
        return commits[0]['commit']['author']['date'].split('T')[0]
    except Exception as e:
        return 'n/a'

def review_candidate(username):
    """
    Branch off of the initial commit and then create a pull request into the new branch
    """
    repo = get_repo_name(username)
    # grab the original commit
    commits = github.list_commits_on_repo(org, repo, org_admin)
    first_commit_sha = commits[-1]['sha']

    branch_name = '{}-review'.format(repo)
    github.create_branch(org, repo, branch_name, first_commit_sha)

    title = 'Code review for {} coding challenge'.format(username)
    head = 'master'
    body = 'Please comment/critique the following code and submit your score as a comment.'
    github.create_pull_request(org, repo, title, head, branch_name, body)

def print_exception(err, prefix="An unexpected error occurred", do_before_trace=None):
    print("{}: {}".format(prefix, err.message))
    if do_before_trace:
        do_before_trace(err)
    print(traceback.format_exc())

def main(args):
    try:
        if (len(args) == 0):
            print("Usage:")
            print("  Create: %s USERNAME" % sys.argv[0])
            print("  Remove: %s --remove USERNAME" % sys.argv[0])
            print("  Review: %s --review USERNAME" % sys.argv[0])
            sys.exit(1)

        username = args.pop(0)
        if username == '--remove':
            username = args.pop(0)
            remove_coding_challenge(username)
        elif username == '--review':
            username = args.pop(0)
            remove_user_from_repo(username)
            review_candidate(username)
        else:
            create_coding_challenge(username)
    except github.requests.exceptions.RequestException as err:
        print_exception(err,
                        "An HTTP error occurred",
                        lambda err: print("HTTP Response: {}".format(err.response.text)))
        sys.exit(1)
    except Exception as err:
        print_exception(err)
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
