import json

import requests

API_TOKEN = "2985a18dde12b2570542c0fd02b6a244643db22245b5c1dc8cd2dcdb9cab543f"
API_KEY = "2aba875333fd26536365c15bf50f02e6"
USER_ID = "6043bf62cad238312f4b2af4"
base_url = "https://api.trello.com"


def getUserInfo(userID):
    user_url = base_url + "/1/members/%s" % userID
    headers = {
        "Accept": "application/json"
    }
    query = {
        'key': API_KEY,
        'token': API_TOKEN
    }
    response = requests.request(
        "GET",
        user_url,
        headers=headers,
        params=query
    )

    # ID, name and email
    print("Printing ID, name and email...")
    print(response.json()['id'])
    print(response.json()['username'])
    print(response.json()['email'])

    boards_url = base_url + "/1/members/%s/boards" % userID
    headers = {
        "Accept": "application/json"
    }
    query = {
        'key': API_KEY,
        'token': API_TOKEN
    }
    response = requests.request(
        "GET",
        boards_url,
        headers=headers,
        params=query
    )
    data = response.text
    parsed = json.loads(data)
    print("Printing boards name and url...")
    for obj in parsed:
        print(obj['name'], obj['url'])


getUserInfo(USER_ID)
