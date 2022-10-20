import requests

url = "https://api.notion.com/v1/databases/todos-472716bb9fca4d05a32bdd20d65d187f/query"

payload = {
    "page_size": 100,
    "filter": {"and": [{
                "property": "Done",
                "checkbox": {"equals": True}
            }, {"or": [
                    {
                        "property": "Tags",
                        "contains": "A"
                    },
                    {
                        "property": "Tags",
                        "contains": "B"
                    }
                ]}]}
}
headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)