# @Time    : 11/03/2021 12:30
# @Author  : Rosangela Kelwattes
# @Email   : l00162027@student.lyit.ie
import json
from datetime import timedelta, date

import requests

API_TOKEN = "2985a18dde12b2570542c0fd02b6a244643db22245b5c1dc8cd2dcdb9cab543f"
API_KEY = "2aba875333fd26536365c15bf50f02e6"
base_url = "https://api.trello.com"


class Endpoints:

    @classmethod
    def getUserInfo(cls, userID):

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
        data = response.text
        parsed = json.loads(data)
        # ID, name and email
        print("User details :")
        print(response.json()['id'])
        print(response.json()['email'])
        print(response.json()['username'])
        response = cls.getBoards(userID)
        data = response.text
        parsed = json.loads(data)
        print("User Boards")
        for obj in parsed:
            print(obj['name'], obj['url'])

    @classmethod
    def getBoards(cls, userID):

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
        return response

    @classmethod
    def createNewBoard(cls, boardName, boardDescription):
        board_url = base_url + "/1/boards/"
        query = {
            'key': API_KEY,
            'token': API_TOKEN,
            'name': boardName,
            'desc': boardDescription
        }

        response = requests.request(
            "POST",
            board_url,
            params=query
        )

        return response

    @classmethod
    def addToDoItems(cls, boardName, teamMemberName):

        response = cls.getUser()
        data = response.text
        parsed = json.loads(data)
        userId = parsed['id']

        response = cls.getBoards(userId)
        data = response.text
        parsed = json.loads(data)
        for i in parsed:
            if i['name'] == boardName:
                idBoard = i['id']
                break

        response = cls.getList(idBoard)
        todoList = response.json()[0]['id']
        name = teamMemberName + "'s list"
        description = "New work for Tom"

        # add a card called
        # “Tom’s list” with a description “New work for Tom”
        response = cls.createCard(name, description, todoList)
        data = response.text
        parsed = json.loads(data)
        idCard = parsed['id']

        # The Card should have a Due Date of 1 week from today.
        cls.updateCardDueDate(idCard)

        # The Card should contain two Checklists named “Key tasks” and “Additional tasks”
        Key_tasks_response = cls.createCheckList("Key tasks", idCard)
        idKeyTasks = Key_tasks_response.json()['id']
        Additional_tasks_response = cls.createCheckList("Additional tasks", idCard)
        idAdditionalTasks = Additional_tasks_response.json()['id']

        # The check list “Key tasks” should have two items called “Key task 1”, “Key task 2”
        cls.createCheckItem(idKeyTasks, "Key task 1")
        cls.createCheckItem(idKeyTasks, "Key task 2")
        # The “Additional tasks” checklist should have two items called “Additional task 1” and “Additional task 2”
        cls.createCheckItem(idAdditionalTasks, "Additional task 1")
        cls.createCheckItem(idAdditionalTasks, "Additional task 2")

    @classmethod
    def moveCardToNewList(cls, idCard, idNewList):

        moverCard_urls = base_url + "/1/cards/%s" % idCard
        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': API_KEY,
            'token': API_TOKEN,
            'idList': idNewList
        }
        response = requests.request(
            "PUT",
            moverCard_urls,
            headers=headers,
            params=query
        )
        return response

    @classmethod
    def getAFieldOnACard(cls, idCard, field):

        cardFiled_url = base_url + "/1/cards/%s/%s" % (idCard, field)
        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }
        response = requests.request(
            "GET",
            cardFiled_url,
            headers=headers,
            params=query
        )
        return response

    @classmethod
    def updateItem(cls, boardName, checkListItemName, isComplete):
        # Search the board for the named list item, eg “Key task 1”,
        # and update the Checklist item using the isComplete parameter.
        response = cls.getUser()
        data = response.text
        parsed = json.loads(data)
        userId = parsed['id']

        response = cls.getBoards(userId)
        data = response.text
        parsed = json.loads(data)
        for i in parsed:
            if i['name'] == boardName:
                idBoard = i['id']
                break
        response = cls.getCards(idBoard)
        idCard = response.json()[0]['id']
        print(idCard)

        response = cls.getCard(idCard)
        data = response.text
        parsed = json.loads(data)
        for i in parsed:
            checkItem = i['checkItems']
            for j in checkItem:
                if j['name'] == checkListItemName:
                    idCheckItem = j['id']
                    print(idCheckItem)
        cls.udateCheckListItemStatus(idCard, idCheckItem, "complete")
        response = cls.getCompletedCheckListItems(idCard)
        data = response.text
        parsed = json.loads(data)
        numberOfCompletedCheckItems: int = len(parsed)

        response = cls.getAFieldOnACard(idCard, "badges")
        data = response.text
        parsed = json.loads(data)
        totalNumberOfCheckItems: int = parsed['checkItems']

        response = cls.getList(idBoard)
        todoList = response.json()[0]['id']
        doingList = response.json()[1]['id']
        doneList = response.json()[2]['id']

        if numberOfCompletedCheckItems > 0 and numberOfCompletedCheckItems < totalNumberOfCheckItems:
            cls.moveCardToNewList(idCard, doingList)
        elif numberOfCompletedCheckItems == totalNumberOfCheckItems:
            cls.moveCardToNewList(idCard, doneList)
        else:
            cls.moveCardToNewList(idCard, todoList)

    @classmethod
    def udateCheckListItemStatus(cls, idCard, idCheckItem, isComplete):
        curr_url = base_url + "/1/cards/%s/checkItem/%s" % (idCard, idCheckItem)
        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }
        payload = {
            "state": isComplete
        }
        response = requests.request(
            "PUT",
            curr_url,
            headers=headers,
            params=query,
            data=payload
        )

    @classmethod
    def getCompletedCheckListItems(cls, idCard):

        completedCheckListItems_url = base_url + "/1/cards/%s/checkItemStates" % idCard
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }

        response = requests.request(
            "GET",
            completedCheckListItems_url,
            params=query
        )
        return response

    @classmethod
    def getCheckListItems(cls, checklist):

        checkItem_url = base_url + "/1/checklists/%s/checkItems" % checklist
        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }
        response = requests.request(
            "GET",
            checkItem_url,
            headers=headers,
            params=query
        )
        return response

    @classmethod
    def createCheckItem(cls, idCheckList, name):
        item_url = base_url + "/1/checklists/%s/checkItems" % idCheckList
        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }
        payload = {
            "name": name,
        }
        response = requests.request(
            "POST",
            item_url,
            params=query,
            data=payload)
        return response

    @classmethod
    def createCheckList(cls, name, idCard):

        checklist_url = base_url + "/1/checklists"
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }
        payload = {
            "name": name,
            "idCard": idCard
        }
        response = requests.request(
            "POST", checklist_url,
            params=query,
            data=payload)

        return response

    @classmethod
    def getCard(cls, idCard):

        checklist_url = base_url + "/1/cards/%s/checklists" % idCard
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }

        response = requests.request(
            "GET", checklist_url,
            params=query)

        return response

    @classmethod
    def updateCardDueDate(cls, idCard):
        update_card_url = base_url + "/1/cards/%s" % idCard
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }
        EndDate = date.today() + timedelta(days=7)
        payload = {"due": EndDate}
        response = requests.request("PUT", update_card_url, params=query, data=payload)
        return response

    @classmethod
    def createCard(cls, name, desc, idList, ):

        card_url = base_url + "/1/cards/"
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }
        payload = {"name": name, "desc": desc, "idList": idList}
        response = requests.request("POST", card_url, params=query, data=payload)

        return response

    @classmethod
    def getCards(cls, idBoard):

        card_url = base_url + "/1/boards/%s/cards" % idBoard
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }
        response = requests.request(
            "GET",
            card_url,
            params=query)

        return response

    @classmethod
    def getUser(cls):
        user_url = base_url + "/1/members/me"
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }
        response = requests.request(
            "GET",
            user_url,
            params=query
        )
        return response

    @classmethod
    def getList(cls, idBoard):

        list_url = base_url + "/1/boards/%s/lists" % idBoard
        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': API_KEY,
            'token': API_TOKEN
        }
        response = requests.request(
            "GET",
            list_url,
            headers=headers,
            params=query
        )
        return response
