import json
import os

from flask import Flask, request, flash, render_template, abort, redirect, url_for, jsonify, g, session 
from flask.ext.github import GitHub

from method_rewrite_middleware import MethodRewriteMiddleware
import coding_challenge

import github as github_admin_api

app = Flask(__name__)

app.secret_key = '\xa5m\xc9?\xd3\x92\xfc>\xc9<\x8f\xed\x86lp=\xe6R\xec\xe4\xde\xda\x0f\xea' # TODO: not so secret - pull out into env
app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)

app.config['GITHUB_CLIENT_ID'] = os.getenv('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.getenv('GITHUB_CLIENT_SECRET')
github = GitHub(app)

app.config['DEBUG'] = bool(int(os.getenv('DEBUG', 1)))

@app.route("/")
def index():
    challenges = [{
                    'repo_name': c['name'],
                    'username': ''.join(c['name'].split('challenge-')[1:]),
                    'html_url': c['html_url'],
                    'language': c['language']
                  } for c in coding_challenge.list_coding_challenges()]
    return render_template('index.html', challenges=challenges)

@app.route("/assignment/new", methods=['GET'])
def new_assignment():
    return render_template('assign.html')

@app.route("/assignment", methods=['POST'])
def create_assignment():
    username = request.form['github-username']
    try:
        candidate, team, repo = coding_challenge.create_coding_challenge(username)
        flash('GitHub user "{}" assigned to the coding challenge! They should submit their work to {}'.format(username, repo['html_url']), 'success')
    except github_admin_api.requests.exceptions.RequestException as err:
        flash('Error: {}'.format(json.loads(err.response.text)['message']), 'error')
    return redirect('/')

@app.route("/assignment/<username>", methods=['DELETE'])
def delete_assignment(username):
    try:
        coding_challenge.remove_coding_challenge(username)
        flash('Removed coding challenge for {}'.format(username), 'success')
    except github_admin_api.requests.exceptions.RequestException as err:
        flash('Error: {}'.format(json.loads(err.response.text)['message']), 'error')
    return redirect('/')

@app.route("/search/users", methods=['GET'])
def search_users():
    q = request.args.get('q')
    users = coding_challenge.search_users(q)
    return json.dumps(users)

@app.before_request
def before_request():
    if request.path == '/github-callback':
        return
    if session.get('github_access_token', None) is None:
        return github.authorize()
    g.user = github.get('user')
    if not is_authorized():
        return render_template('unauthorized.html'), 401

@github.access_token_getter
def token_getter():
    return session.get('github_access_token', None)

def is_authorized():
    return is_org_member(coding_challenge.org) and any(map(is_team_member, coding_challenge.team_ids))

def is_org_member(org):
    return len([o for o in github.get('users/{}/orgs'.format(g.user['login'])) if o['login'] == org]) == 1

def is_team_member(team_id):
    r, status = github_admin_api.get_team_membership(team_id, g.user['login'])
    return status == 200 and r['state'] == 'active'

@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        return render_template('unauthorized.html'), 401
    session['github_access_token'] = oauth_token
    return redirect(next_url)

if __name__ == "__main__":
    app.run()
