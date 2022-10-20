import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()


url = "https://api.notion.com/v1/databases/e19eff6dfb4745919abd6cfd66dc54f2/query"

payload = {
    "page_size": 100,
    "filter": {
        "and": [
            {"property": "Completed", "checkbox": {"equals": False}}#,
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
    "authorization": os.getenv('TOKEN')
}

response = requests.post(url, json=payload, headers=headers)

# print(response.text)

data = json.loads(response.text)

item = data["results"][0]
print(item)

json_formatted_str = json.dumps(item, indent=2)

print(json_formatted_str)