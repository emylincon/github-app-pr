import os
from flask import Flask, request
from github import Github, GithubIntegration


app = Flask(__name__)

# Read Environment Variables
app_id = os.getenv("app_id")
app_private_key = os.environ.get("app_private_key")


# Create an GitHub integration instance
git_integration = GithubIntegration(
    app_id,
    app_private_key,
)


@app.route("/", methods=["GET"])
def home():
    return "Hello 👋"


@app.route("/", methods=["POST"])
def bot():
    # Get the event payload
    payload = request.json

    # Check if the event is a GitHub PR creation event
    if (
        not all(k in payload.keys() for k in ["action", "pull_request"])
        and payload["action"] == "opened"
    ):
        return "ok"

    owner = payload["repository"]["owner"]["login"]
    repo_name = payload["repository"]["name"]

    # Get a git connection as our bot
    # Here is where we are getting the permission to talk as our bot and not
    # as a Python webservice
    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(owner, repo_name).id
        ).token
    )
    repo = git_connection.get_repo(f"{owner}/{repo_name}")

    issue = repo.get_issue(number=payload["pull_request"]["number"])

    # Create a comment on the PR
    issue.create_comment(f":rainbow: Thanks for creating this PR :rocket:")

    # Add a Label to the PR
    issue.set_labels("enhancement")

    # Approve PR
    pr = repo.get_pull(number=payload["pull_request"]["number"])
    commit = repo.get_commit(pr.head.sha)
    pr.create_review(commit=commit, body="Approved  👍", event="APPROVE")

    return "ok"


# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
