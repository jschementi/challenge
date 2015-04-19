# SOLS Coding Challenge

Assigns the coding challenge to a specific GitHub user,
by making them their own GitHub repository to push their answers to.

## Setup

In [Terminal.app](http://en.wikipedia.org/wiki/Terminal_%28OS_X%29), run:

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
echo "export PATH=/usr/local/bin:/usr/local/sbin:$PATH" >> ~/.profile
source ~/.profile
brew install python
git clone https://github.com/SolsCo/challenge.git
cd challenge
pip install -r requirements
```

> NOTE: You'll be prompted to install Xcode command-line tools if you don't
> already have them installed.

## Usage

Assign the coding challenge to a GitHub username:

```
./coding_challenge <github-username>
```

After their interview process is complete and we no longer need to reference
their solutions, you can unassign the coding challenge:

```
./coding_challenge --remove <github-username>
```

