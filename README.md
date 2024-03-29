# Github App for PRs ![Build](https://img.shields.io/github/actions/workflow/status/emylincon/github-app-pr/python-package.yml?branch=main)
This is a basic app for handling PRs. The following are the app's functionalities
* Label PR
* Comment on PR
* Approve PR  ⚠️ <span style="color:red; font-style:italic; font-size: 11px">(If Repo is private, ensure `Contents read only` permission is granted)</span>

## Permissions and Events Required
### Repository Permissions
* Metadata : `READ ONLY`
* Issues : `READ & WRITE`
* Pull Request: `READ & WRITE`
* Contents: `READ ONLY` (Only required for private repos)

### Events Permissions
- [x] Pull Request


## Getting Started
* Create github app
* Create python environment
```bash
python3 -m venv venv
```
* Activate environment
```bash
source venv/bin/activate
```
* export environment variables
```
export app_id="XXXXX"
export app_private_key="contents-of-private_key.pem-file"
```
* Install app requirements
```
pip3 install -r requirements
```
* Run app
```
flask run
```

# Dev Test
* use ngrok to get internet facing webhook url to test locally
```
ngrok http 5000
```

## Useful Resources
* [Github Apps CheatSheet](https://github.com/github-developer/github-apps-cheat-sheet/blob/master/README.md)
* [Github app Libraries](https://docs.github.com/en/rest/overview/libraries)
* [Creating Github App](https://www.youtube.com/watch?v=iaBEWB1As0k)
