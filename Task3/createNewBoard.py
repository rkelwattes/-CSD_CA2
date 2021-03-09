# @Time    : 07/03/2021 22:38
# @Author  : Rosangela Kelwattes
# @Email   : l00162027@student.lyit.ie
import requests

API_TOKEN = "2985a18dde12b2570542c0fd02b6a244643db22245b5c1dc8cd2dcdb9cab543f"
API_KEY = "2aba875333fd26536365c15bf50f02e6"
USER_ID = "6043bf62cad238312f4b2af4"
base_url = "https://api.trello.com"


def createNewBoard(name, desc):
    board_url = base_url + "/1/boards/"
    query = {
        'key': API_KEY,
        'token': API_TOKEN,
        'name': name,
        'desc': desc

    }

    response = requests.request(
        "POST",
        board_url,
        params=query
    )

    response = response.json()['id']
    print(response)
    return response


name = 'New Test Board'
desc = 'Board to test board creation'
createNewBoard(name, desc)
