import os
import requests
from dotenv import load_dotenv
import json
import argparse

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--datatype", help="select from 'incomplete'")
parser.add_argument("--datatype", help="", required=False)
args = parser.parse_args()


url = "https://api.notion.com/v1/databases/e19eff6dfb4745919abd6cfd66dc54f2/query"

payload = {
    "page_size": 100,
    "filter": {
        "and": [
            {"property": "Completed", "checkbox": {"equals": False}}  # ,
            # {
            #     "or": [
            #         {"property": "Tags", "contains": "A"},
            #         {"property": "Tags", "contains": "B"},
            #     ]
            # },
        ]
    },
}
headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "authorization": os.getenv("TOKEN"),
}

response = requests.post(url, json=payload, headers=headers)

# print(response.text)

data = json.loads(response.text)

item = data["results"]
print(item)
