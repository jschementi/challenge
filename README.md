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
git clone https://github.com/SolsCo/challenge.git
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

The [app is deployed to AWS](http://ec2-52-4-137-245.compute-1.amazonaws.com) with
[Riker](http://github.com/jschementi/riker). [Jenkins](http://ec2-52-5-135-159.compute-1.amazonaws.com:8080/job/coding-challenge-admin/)
performs the deployment on each push to this repository.

## Command-Line Setup & Usage

`coding-challenge.py` can also be used as a command-line tool.

### Setup

In [Terminal.app](http://en.wikipedia.org/wiki/Terminal_%28OS_X%29), run:

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
echo "export PATH=/usr/local/bin:/usr/local/sbin:$PATH" >> ~/.profile
source ~/.profile
brew install python
git clone https://github.com/SolsCo/challenge.git
cd challenge
pip install -r requirements.txt
```

> NOTE: You'll be prompted to install Xcode command-line tools if you don't
> already have them installed.

### Usage

Assign the coding challenge to a GitHub username:

```
./coding_challenge <github-username>
```

After their interview process is complete and we no longer need to reference
their solutions, you can unassign the coding challenge:

```
./coding_challenge --remove <github-username>
```

