# Coding Challenge

Assigns the coding challenge to a specific GitHub user,
by making them their own GitHub repository to push their answers to.

## Setup Locally

### Install Python and Foreman on OS X

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
echo "export PATH=/usr/local/bin:/usr/local/sbin:$PATH" >> ~/.profile
source ~/.profile
brew install python
sudo gem install foreman
```

### Clone Repo

```
git clone https://github.com/jschementi/challenge.git
cd challenge
```

### Install Python packages

```
pip install -r requirements.txt
```

### Run web server

```
foreman start
```

Open [http://localhost:5000](http://localhost:5000) in web browser.

## Deploy

This app can easily be deployed to Heroku, Digital Ocean w/Dokku,
AWS Elastic Beanstalk, or your own custom server.

## Command-Line Setup & Usage

`coding-challenge.py` can also be used as a command-line tool.

### Setup

In [Terminal.app](http://en.wikipedia.org/wiki/Terminal_%28OS_X%29), run:

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
echo "export PATH=/usr/local/bin:/usr/local/sbin:$PATH" >> ~/.profile
source ~/.profile
brew install python
git clone https://github.com/jschementi/challenge.git
cd challenge
pip install -r requirements.txt
```

> NOTE: You'll be prompted to install Xcode command-line tools if you don't
> already have them installed.

## Configuration

```bash
cp example.env .env
```

Then set the following environment variables:

| Variable                    |                  Example                 | Description                                                                                                               |
|-----------------------------|:----------------------------------------:|---------------------------------------------------------------------------------------------------------------------------|
| GITHUB_CLIENT_ID            |           1234567890abcdefghij           | [Github OAuth Client ID](https://github.com/settings/developers)                                                         |
| GITHUB_CLIENT_SECRET        | 1234567890abcdef1234567890abcdef12345678 | [Github OAuth Client Secret](https://github.com/settings/developers)                                                     |
| GITHUB_TOKEN                | 1234567890abcdef1234567890abcdef12345678 | [Generate Personal Access Token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) |
| GITHUB_ORG                  |                  OrgName                 | Name of your github organization                                                                                          |
| GITHUB_ADMIN                |                 UserName                 | Name of your github admin                                                                                                 |
| HOMEPAGE                    |            https://github.com/           | Homepage of your organization                                                                                             |
| SECRET_KEY                  |            SecretPassword12345           | A secret key for your installation, perhaps generated via `openssl rand -hex 32`                                          |
| GITHUB_ENGINEERING_TEAM     |              EngineeringTeam             | The github team for your engineers                                                                                        |
| GITHUB_RECRUITING_TEAM      |              RecruitingTeam              | The github team for your recruiters                                                                                       |

### Usage

Assign the coding challenge to a GitHub username:

```
./coding_challenge <github-username>
```

Remove the candidate from the repo and create a pull request for the team to review:

```
./coding_challenge --review <github-username>
```

After their interview process is complete and we no longer need to reference
their solutions, you can unassign the coding challenge:

```
./coding_challenge --remove <github-username>
```
