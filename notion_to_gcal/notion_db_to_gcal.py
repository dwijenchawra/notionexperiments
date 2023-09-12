import requests
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pprint import pprint
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

load_dotenv()

# Set your Notion API token and database ID from .env file
NOTION_API_TOKEN = os.environ.get('NOTION_API_TOKEN')
DATABASE_ID = os.environ.get('DATABASE_ID')

# Set your Google Calendar API credentials JSON file path
GOOGLE_CREDENTIALS_FILE = os.environ.get('GCAL_CREDENTIALS_FILE')

REFRESH_TIME = 15  # seconds

print(GOOGLE_CREDENTIALS_FILE)

# Define the Notion API endpoints
NOTION_API_URL = 'https://api.notion.com/v1'
DATABASE_ENDPOINT = f'{NOTION_API_URL}/databases/{DATABASE_ID}/query'

# Set headers for the Notion API request
headers = {
    'Authorization': f'Bearer {NOTION_API_TOKEN}',
    'Notion-Version': '2021-05-13',
    'Content-Type': 'application/json',
}


r = requests.post(DATABASE_ENDPOINT, headers={
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Notion-Version": "2021-08-16"
  })

# result_dict = r.json()
# pprint(result_dict)
# movie_list_result = result_dict['results']

# pprint(movie_list_result)

# Initialize the Google Calendar API client
credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_FILE, scopes=['https://www.googleapis.com/auth/calendar']
)
calendar_service = build('calendar', 'v3', credentials=credentials)

while True:
    try:
        # Calculate the start time for the refresh interval
        start_time = datetime.now() - timedelta(seconds=REFRESH_TIME)
        start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S%z')

        print(f"Fetching entries edited after: {start_time_str}")

        # Create a filter to get entries edited in the last refresh interval
        filter_params = {
            'property': 'Last edited time',
            'date': {
                'on_or_after': start_time_str
            }
        }

        # Make a request to fetch database entries edited in the last interval
        response = requests.post(DATABASE_ENDPOINT, headers=headers, json={'filter': filter_params})

        # Check for a successful response
        if response.status_code == 200:
            data = response.json()
            pprint(data)

            # Process the retrieved data and create Google Calendar events
            results = data.get('results', [])
            for item in results:
                # Extract relevant data from the Notion item
                title = item.get('properties', {}).get('title', {}).get('title', [])
                due_date = item.get('properties', {}).get('due_date', {}).get('date', None)
                status = item.get('properties', {}).get('status', {}).get('select', {}).get('name', '')

                if title and due_date and status.lower() != 'done':
                    # Create a Google Calendar event using the due date
                    event = {
                        'summary': title,
                        'start': {'date': due_date},
                        'end': {'date': due_date},
                    }

                    # Insert the event into the Google Calendar
                    # calendar_service.events().insert(calendarId='primary', body=event).execute()
                    print(f"Created event: {title} on {due_date}")

        else:
            print(f"Error: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Wait for the next refresh interval 
    time.sleep(REFRESH_TIME)
    print("Refreshing...")
