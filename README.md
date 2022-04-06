# Slack - Audit Channels with Guests
This is a super simple tool that prints out a list of guest accounts and the public channels they’re a member of.

### Requirements
* python3
* Install requirements.txt ( pip install -r requirements.txt )
* An  [OAuth token](https://api.slack.com/docs/oauth)  from a  [Slack app](https://api.slack.com/slack-apps)  on your workspace that has the following permission scopes:
**Bot Token Scopes**
* channels:read
* users:read
* [optional] users:read:email

Add the Bot User OAuth Token in config.env.

### Usage
python guest_channels.py

### Docker
* First build the docker image (in the root of the project)
docker build —tag slackguests .
* run the container
docker run slackguests
