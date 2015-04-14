# SOLS Coding Challenge

Assigns the coding challenge to a specific GitHub user,
by making them their own GitHub repository to push their answers to.

## Setup

In [Terminal.app](http://en.wikipedia.org/wiki/Terminal_%28OS_X%29), run:

```
git clone https://github.com/SolsCo/challenge.git
cd challenge
sudo pip install -r requirements
```

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

