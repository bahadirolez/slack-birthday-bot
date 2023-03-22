import os
import datetime
import ssl
import certifi
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

# Fetch Slack API token from environment variable
SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]

# Fetch spreadsheet ID and channel name from environment variables
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]

# Create an SSL context that uses the 'certifi' package's CA bundle
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Authenticate with Google Sheets API using a service account
def get_google_sheets_service_account():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    credentials = service_account.Credentials.from_service_account_file("service_account_key.json", scopes=scopes)
    service = build("sheets", "v4", credentials=credentials)
    return service

# Fetch birthdays from Google Sheets
def get_birthdays(service):
    range_name = "Sheet1!A2:C"
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    rows = result.get("values", [])
    return rows

# Find a Slack user by email address
def find_user_by_email(slack_client, email):
    try:
        response = slack_client.users_lookupByEmail(email=email)
        return response["user"]["id"]
    except SlackApiError as e:
        print(f"Error finding user by email {email}: {e}")
        return None

# Send a birthday message to the specified Slack Channel
def send_birthday_message(slack_client, user_id, name):
    try:
        message = f"Hello <!channel>, today is a special day for <@{user_id}>! 🎂 Happy birthday <@{user_id}>! 🥳"
        response = slack_client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        print(f"Message sent: {response['ts']}")
    except SlackApiError as e:
        print(f"Error sending message: {e}")

# Check for birthdays and send messages if necessary
def check_and_send_birthday_messages():
    today = datetime.datetime.now().strftime("%m-%d")

    sheets_service = get_google_sheets_service_account()
    birthdays = get_birthdays(sheets_service)

    slack_client = WebClient(token=SLACK_API_TOKEN, ssl=ssl_context)

    for row in birthdays:
        name, birthday, email = row
        birthday_month_day = datetime.datetime.strptime(birthday.strip(), "%Y-%m-%d").strftime("%m-%d")
        if birthday_month_day == today:
            user_id = find_user_by_email(slack_client, email)
            if user_id:
                send_birthday_message(slack_client, user_id, name)

if __name__ == "__main__":
    check_and_send_birthday_messages()
