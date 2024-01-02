from helpers.utils import write_down_to_txt
from DB.pile import MongoDBOwnPile
import requests
import os


class ApiURLInitializer(MongoDBOwnPile):
    METALS_LIST = ['XAG', 'XAU']

    def __init__(self):
        super().__init__()
        self.BASIC_URL = 'https://api.metalpriceapi.com/'
        self.CONVERT_URL = 'v1/convert'
        self.QUANTITY = self.list_of_ore_weight()
        self.TOKEN = os.getenv('TOKEN')


class ApiConverters:

    def __init__(self):
        self.api_gate = ApiURLInitializer()
    def convert_url(self):
        url = f'{self.api_gate.BASIC_URL}{self.api_gate.CONVERT_URL}'
        return url

    def convert_request(self):
        treasure_chest = []
        headers = {
            'Content-type': 'application/json'
        }
        for (q, m) in zip(self.api_gate.QUANTITY, self.api_gate.METALS_LIST):
            payload = {
                'api_key': self.api_gate.TOKEN,
                'from': m,
                'to': 'PLN',
                'amount': q
            }
            response = requests.get(self.convert_url(), headers=headers, params=payload).json()
            treasure_chest.append(m + " {:,.2f}".format(response['result']) + " PLN")
        return treasure_chest


write_down_to_txt(ApiConverters().convert_request())
