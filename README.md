# lunchbot
Post today's lunch to Slack.

## Installation
Put this script in a folder, chmod the file and replace the variable webhook_url with a URL to your Slack channel.
Add a new line to crontab (`$ crontab -e`).
`30 10 * * 1-5 /path/to/script/get-lunch.py`
