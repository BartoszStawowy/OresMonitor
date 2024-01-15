from Helpers.utils import write_down_to_txt
from DB.pile import MongoDBOwnPile
from dataclasses import dataclass
import requests
import os

@dataclass
class ApiURLInitializer():
    # Endpoint with actual ores prices #
    METALS_LIST = ['XAG', 'XAU']
    BASIC_URL: str = 'https://api.metalpriceapi.com/'
    CONVERT_URL: str = 'v1/convert'
    TOKEN: str = os.getenv('TOKEN')


class ApiConverters:

    def __init__(self):
        self.api_gate = ApiURLInitializer()
        self.mongo_db_pile = MongoDBOwnPile()

    def convert_url(self):
        url = f'{self.api_gate.BASIC_URL}{self.api_gate.CONVERT_URL}'
        return url

    def convert_request(self):
        # count all user ore's, check weight market value adn write down to result.txt #
        treasure_chest = []
        headers = {
            'Content-type': 'application/json'
        }
        for (quantity, metal) in zip(self.mongo_db_pile.list_of_ore_weight(), self.api_gate.METALS_LIST):
            payload = {
                'api_key': self.api_gate.TOKEN,
                'from': metal,
                'to': 'PLN',
                'amount': quantity
            }
            response = requests.get(self.convert_url(), headers=headers, params=payload).json()
            treasure_chest.append(metal + " {:,.2f}".format(response['result']) + " PLN")
        self.mongo_db_pile.mongo_connection.mongo_killer()
        return treasure_chest


# write_down_to_txt(ApiConverters().convert_request())
