import os
from flask import Flask, request
from github import Github, GithubIntegration


app = Flask(__name__)
TABLE = {}  # ! schema: {pull_request_url: true} {str: bool}

# Read Environment Variables
app_id = os.getenv("app_id")
app_private_key = os.environ.get("app_private_key")

# Verify credentials are set
for key, value in {"app_id": app_id, "app_private_key": app_private_key}.items():
    if not value:
        print(
            f"[ERROR]: Credentials Not Set - '{key}'\n\tPlease run: \n\texport {key}='somevalue'")
        quit(1)


# Create an GitHub integration instance
git_integration = GithubIntegration(
    app_id,
    app_private_key,
)


def error_handler(e: Exception, kind: str = "CRITICAL") -> str:
    err = f"[ERROR][{kind}]: {e.__class__} | message: {e}"
    print(err)
    print(f"[ERROR DETAILS][{kind}]: {e.__traceback__}")
    return err


@app.route("/", methods=["GET"])
def home():
    return "Hello 👋"


@app.route("/", methods=["POST"])
def bot():
    # * Get the event payload
    payload = request.json

    # * Check if the event is a GitHub PR creation event
    if (
        not all(k in payload.keys() for k in ["action", "pull_request"])
        and payload["action"] == "opened"
    ):
        return "ok"

    try:
        owner = payload["repository"]["owner"]["login"]
        repo_name = payload["repository"]["name"]
        pr_url = payload["pull_request"]["html_url"]
        pr_state = payload["pull_request"]["state"]
    except Exception as e:
        return error_handler(e, "PAYLOAD")

    # if request has not been processed and PR state is open
    if not TABLE.get(pr_url) and pr_state == "open":
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

        # Add a Label to the PR
        try:
            issue.set_labels("enhancement")
        except Exception as e:
            error_handler(e, "ADD LABEL")

        # Create a comment on the PR
        try:
            issue.create_comment(
                f":rainbow: Thanks for creating this PR :rocket:")
        except Exception as e:
            error_handler(e, "CREATE COMMENT")

        # set Pull request to processed
        TABLE[pr_url] = True

        # Approve PR
        try:
            pr = repo.get_pull(number=payload["pull_request"]["number"])
            commit = repo.get_commit(pr.head.sha)
            pr.create_review(
                commit=commit, body="Approved  👍", event="APPROVE")
        except Exception as e:
            return error_handler(e, "APPROVE PULL REQUEST")
    else:
        print("[INFO]: REQUEST HAS BEEN PREVIOUSLY SUBMITTED")

    return "ok"


# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
