# @Time    : 07/03/2021 22:37
# @Author  : Rosangela Kelwattes
# @Email   : l00162027@student.lyit.ie
import json
import requests
from datetime import timedelta, date

API_TOKEN = "2985a18dde12b2570542c0fd02b6a244643db22245b5c1dc8cd2dcdb9cab543f"
API_KEY = "2aba875333fd26536365c15bf50f02e6"
USER_ID = "6043bf62cad238312f4b2af4"
base_url = "https://api.trello.com"


def addToDoItems(boardname, teamMemberName):

    boards_url = base_url + "/1/members/%s/boards" % USER_ID
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
    print(data)
    parsed = json.loads(data)

    # Define a function to search the item
    for i in parsed:
        if i['name'] == boardname:
            idBoard = i['id']
            print(idBoard)
            break
    list_url = base_url + "/1/boards/%s/lists" % idBoard
    response = requests.request(
        "GET",
        list_url,
        headers=headers,
        params=query
    )

    data = response.text
    print(data)
    card_url = base_url + "/1/cards/"
    idList = response.json()[0]['id']
    print(idList)
    teamMemberName = teamMemberName + "'s list"
    description = "New work for Tom"
    payload = {"name": teamMemberName, "desc": description, "idList": idList}
    response = requests.request("POST", card_url, params=query, data=payload)

    data = response.text
    print(data)
    idCard = response.json()['id']
    print(idCard)
    update_card_url = base_url + "/1/cards/%s" % idCard
    EndDate = date.today() + timedelta(days=7)
    payload = {"due": EndDate}
    response = requests.request("PUT", update_card_url, params=query, data=payload)
    data = response.text
    print(data)

    checklist_url = base_url + "/1/checklists"
    payload = {
        "name": "Key tasks",
        "idCard": idCard
    }
    response = requests.request("POST", checklist_url, params=query, data=payload)
    data = response.text
    print(data)
    idCheckList = response.json()['id']
    item_url = base_url + "/1/checklists/%s/checkItems" % idCheckList
    payload = {
        "name": "Key task 1",
    }
    response = requests.request("POST", item_url, params=query, data=payload)
    payload = {
        "name": "Key task 2",
    }
    response = requests.request("POST", item_url, params=query, data=payload)
    payload = {
        "name": "Additional tasks",
        "idCard": idCard
    }
    response = requests.request("POST", checklist_url, params=query, data=payload)
    data = response.text
    print(data)
    idCheckList = response.json()['id']
    item_url = base_url + "/1/checklists/%s/checkItems" % idCheckList
    payload = {
        "name": "Additional task 1",
    }
    response = requests.request("POST", item_url, params=query, data=payload)
    payload = {
        "name": "Additional task 2",
    }
    response = requests.request("POST", item_url, params=query, data=payload)


boardName = 'New Test Board'
teamMemberName = "Tom"

addToDoItems(boardName, teamMemberName)
