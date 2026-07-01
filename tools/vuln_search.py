"""Script to search for repos affected by an undisclosed vulnerability.

1. Update TOKEN, SEARCH_TERM and REPO.
2. Import and run the save_dependents() function if this has not been done before (or within the last year).
3. Execute the script.
4. Use MIN_STARS/OFFSET to adjust how many dependents to search and resume from an interrupted search.
"""

import json
from itertools import takewhile
from pathlib import Path
from time import sleep

import requests
from github_dependents_info.gh_dependents_info import GithubDependentsInfo

# https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api#authenticating-with-a-personal-access-token
TOKEN = "github_pat_XXX"
SEARCH_TERM = ""  # What to use in code search.
REPO = "aiohttp"
MIN_STARS = 100  # Only search for repos with atleast this many stars.
OFFSET = 0  # To resume searching from an interrupted session.

ORG = "aio-libs"
RATE_LIMIT = 60 / 9  # Docs say 10 per minute, but only 9 seem to be allowed.
DEPENDENTS_PATH = Path(f"{REPO}_dependents.json")


def save_dependents():
    """Import and run this function to save the dependents, this may take ~6 hours for a project with 500k dependents."""
    gh_deps_info = GithubDependentsInfo(
        f"{ORG}/{REPO}", sort_key="stars", min_stars=0, json_output=True
    )
    dependents = gh_deps_info.collect()
    with DEPENDENTS_PATH.open("w") as f:
        json.dump(dependents, f, indent=4)


if __name__ == "__main__":
    with DEPENDENTS_PATH.open() as f:
        dependents = json.load(f)

    url = "https://api.github.com/search/code"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
    }
    repos = takewhile(
        lambda r: r["stars"] >= MIN_STARS,
        dependents["all_public_dependent_repos"][OFFSET:],
    )
    for i, repo in enumerate(repos, OFFSET):
        sleep(RATE_LIMIT)
        response = requests.get(
            url, headers=headers, params={"q": f"{SEARCH_TERM} repo:{repo['name']}"}
        )
        response.raise_for_status()

        result = response.json()
        for r in result["items"]:
            print(r["repository"]["full_name"], r["path"])
            print("  ", r["html_url"])

        if i % 100 == 0:
            print("COUNT", i, "({} stars)".format(repo["stars"]))
