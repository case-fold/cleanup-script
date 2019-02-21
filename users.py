#!/usr/bin/env python3
import os
import sys
from github import Github
from urllib.parse import urlsplit

# Read token from env var
if 'GITHUB_TOKEN' not in os.environ:
    print('Environment variable "GITHUB_TOKEN" required.')
    sys.exit(1)

g = Github(os.environ['GITHUB_TOKEN'])

# Get org
nyt = g.get_organization('nytimes')
