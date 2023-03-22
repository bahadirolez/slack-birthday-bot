# Slack Birthday Bot

A Python script that fetches birthday information from a Google Sheet and sends birthday wishes to users in a specified Slack channel.

## Prerequisites

1. Python 3
2. [slack-sdk](https://pypi.org/project/slack-sdk/)
3. [google-auth](https://pypi.org/project/google-auth/)
4. [google-auth-oauthlib](https://pypi.org/project/google-auth-oauthlib/)
5. [google-auth-httplib2](https://pypi.org/project/google-auth-httplib2/)
6. [google-api-python-client](https://pypi.org/project/google-api-python-client/)
7. [certifi](https://pypi.org/project/certifi/)

## Setup

1. Clone this repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. [Create a Google Service Account and obtain the JSON key file](https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount). Save the key file as `service_account_key.json` in the project directory.
4. [Invite the Slack bot to the desired channel](https://www.twilio.com/blog/how-to-build-a-slackbot-in-socket-mode-with-python) and obtain the Slack API token. Set the `SLACK_API_TOKEN` environment variable with the token value.
5. Share your Google Sheet containing the birthday data with the email address associated with the Google Service Account you created earlier.
6. Set the `SPREADSHEET_ID` environment variable with the ID of your Google Sheet.
7. Set the `SLACK_CHANNEL` environment variable with the name of the Slack channel where birthday messages should be sent (e.g., "#general").

## Usage

Run the script with the following command:

```bash
python3 birthday_bot.py
```

To automate the script to run daily at a specific time, you can use a scheduler like cron on Linux or Task Scheduler on Windows.

## Environment Variables

`SLACK_API_TOKEN`: The Slack API token for your bot.
`SPREADSHEET_ID`: The ID of the Google Sheet containing birthday data.
`SLACK_CHANNEL`: The Slack channel where birthday messages should be sent.

## Google Sheet Format

The Google Sheet should have the following columns:
1. name
2. birthday (YYYY-MM-DD format)
3. email

Ensure that there are header rows in the Google Sheet, and the data starts from the second row.

## License

This project is licensed under the MIT License.