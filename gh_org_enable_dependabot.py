import requests
import sys

def authenticate(token):
    headers = {
        "Authorization": f"token {token}"
    }
    return headers

def get_organization_repositories(org, token):
    headers = authenticate(token)
    url = f"https://api.github.com/orgs/{org}/repos"
    repositories = []
    page = 1

    while True:
        params = {"page": page, "per_page": 100}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            repositories += response.json()
            if len(response.json()) < 100:
                break  # Reached the last page
            page += 1
        else:
            print(f"Failed to fetch repositories for organization '{org}'. Status code: {response.status_code}")
            print(response.text)
            break

    return repositories

def enable_dependabot(org, repo, token):
    headers = authenticate(token)
    file_path = "dependabot.yml"
    dependabot_config = """\
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
"""

    # Check if the file already exists
    url = f"https://api.github.com/repos/{org}/{repo}/contents/{file_path}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"'{file_path}' already exists in '{org}/{repo}'.")
        return
    elif response.status_code == 404:
        print(f"'{file_path}' does not exist in '{org}/{repo}'. Creating...")
    else:
        print(f"Failed to check for '{file_path}' in '{org}/{repo}'. Status code: {response.status_code}")
        print(response.text)
        return

    # Create a new branch from main
    branch_url = f"https://api.github.com/repos/{org}/{repo}/git/refs/heads/main"
    response = requests.get(branch_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to get 'main' branch in '{org}/{repo}'. Status code: {response.status_code}")
        print(response.text)
        return

    main_branch_sha = response.json()["object"]["sha"]
    new_branch_name = "enable-dependabot"
    branch_payload = {
        "ref": f"refs/heads/{new_branch_name}",
        "sha": main_branch_sha
    }
    response = requests.post(f"https://api.github.com/repos/{org}/{repo}/git/refs", headers=headers, json=branch_payload)

    if response.status_code != 201:
        print(f"Failed to create branch '{new_branch_name}' in '{org}/{repo}'. Status code: {response.status_code}")
        print(response.text)
        return

    # Create or update dependabot.yml file on the new branch
    content = dependabot_config.encode().decode('utf-8').strip()
    file_payload = {
        "message": "Enable Dependabot",
        "content": content,
        "branch": new_branch_name
    }
    file_response = requests.put(url, headers=headers, json=file_payload)

    if file_response.status_code != 201:
        print(f"Failed to create/update '{file_path}' in '{org}/{repo}'. Status code: {file_response.status_code}")
        print(file_response.text)
        return

    # Create a pull request
    pr_url = f"https://api.github.com/repos/{org}/{repo}/pulls"
    pr_payload = {
        "title": "Enable Dependabot",
        "body": "Automatically enabling Dependabot for automated dependency updates.",
        "head": new_branch_name,
        "base": "main"
    }
    pr_response = requests.post(pr_url, headers=headers, json=pr_payload)

    if pr_response.status_code == 201:
        print(f"Pull request created: {pr_response.json()['html_url']}")
    else:
        print(f"Failed to create pull request. Status code: {pr_response.status_code}")
        print(pr_response.text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python enable_dependabot.py <org> <token>")
        sys.exit(1)

    org = sys.argv[1]
    token = sys.argv[2]

    repositories = get_organization_repositories(org, token)
    for repo in repositories:
        enable_dependabot(org, repo["name"], token)
