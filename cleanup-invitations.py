import os
import requests
import sys
from datetime import datetime

# Fetches pending invitations and returns list of usernames of invitations created days ago
def fetchStaleInvitations(token):
    usernames = []

    # Fetch all pages
    page = 0
    while True:
        page += 1
        r = requests.get(
            'https://api.github.com/orgs/nytimes/invitations',
            params={'page': str(page)},
            headers={'Authorization': 'token ' + token}
        )

        if r.status_code != 200:
            print('failed to fetch invitations', r.status_code, r.text)
            sys.exit(1)

        invitations = r.json()

        # Stop when past last page
        if len(invitations) < 1:
            break

        for inv in invitations:
            # Parse date
            invDate = datetime.strptime(inv['created_at'][:10], '%Y-%m-%d')
            delta = datetime.today() - invDate

            if delta.days >= 3:
                # Add user to list
                usernames.append(inv['login'])
            else:
                # Print invitations that are not included in the result
                print('Recent invitation:', inv['login'], delta.days)

    return usernames

# Remove organization membership
def removeMembership(token, username):
    print('Removing membership %s ...' % user, end='')
    if len(username) < 1:
        return

    r = requests.delete(
        'https://api.github.com/orgs/nytimes/memberships/' + username,
        headers={'Authorization': 'token ' + token}
    )

    if r.status_code == 204:
        print('ok')
    else:
        print('failed. Status:', r.status_code)

if __name__ == "__main__":
    # Read token from env var
    if 'GITHUB_TOKEN' not in os.environ:
        print('Environment variable "GITHUB_TOKEN" required.')
        sys.exit(1)

    ghToken = os.environ['GITHUB_TOKEN']

    usersToRemove = fetchStaleInvitations(ghToken)
    if len(usersToRemove) < 1:
        print('No stale invitations')
        sys.exit(0)

    print('Invitations to remove: ', usersToRemove, '\n[y/n]?')

    if input() != 'y':
        print('Canceled')
        sys.exit(0)

    for user in usersToRemove:
        removeMembership(ghToken, user)
