import requests

url = "https://api.notion.com/v1/databases/database_id/query"

payload = {"page_size": 100}
headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)