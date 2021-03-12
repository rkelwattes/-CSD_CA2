# @Time    : 07/03/2021 22:38
# @Author  : Rosangela Kelwattes
# @Email   : l00162027@student.lyit.ie
import json

from Task3.Endpoints import Endpoints


class Trello:
    USER_ID = "6043bf62cad238312f4b2af4"
    teamMemberName = "Tom"
    name = 'New Test Board'
    desc = 'Board to test board creation'

    # Create board
    response = Endpoints.createNewBoard(name, desc)
    data = response.text
    parsed = json.loads(data)
    idBoard = parsed['id']

    # get getUserInfo
    Endpoints.getUserInfo(USER_ID)
    # get addToDoItems
    Endpoints.addToDoItems(name, teamMemberName)
    # update Item
    Endpoints.updateItem(name, "Key task 1", "complete")
    Endpoints.updateItem(name, "Key task 2", "complete")
    Endpoints.updateItem(name, "Additional task 1", "complete")
    Endpoints.updateItem(name, "Additional task 2", "complete")




