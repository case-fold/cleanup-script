#!/usr/bin/env python3
import os
import sys
from github import Github
from urllib.parse import urlsplit

# Read token from env var
if 'GITHUB_ORG_READ' not in os.environ:
    print('Environment variable "GITHUB_ORG_READ" required.')
    sys.exit(1)

g = Github(os.environ['GITHUB_ORG_READ'])

# Get org
nyt = g.get_organization('nytimes')

# Get teams list
nyt_repos = nyt.get_repos(type="all")
for repo in nyt_repos:
    deploy_keys = repo.get_keys()
    for key in deploy_keys:
        print (repo.name, ',key_id: ', key.id, ', title: ', key.title, ', created_at: ', key.created_at )
