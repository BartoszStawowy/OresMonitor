from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from Helpers.utils import todays_date
from Helpers.re_matches import match_engine
import pymongo
import os

class MongoDBInitializer:
    load_dotenv(find_dotenv())

    # Mongo_db connection. DB data stored in .env #
    def __init__(self):
        self.CLIENT = MongoClient(os.getenv('SERVER'), int(os.getenv('PORT')))
        self.DB = self.CLIENT.Ores
        self.AUX_COLLECTION = self.DB[os.getenv('AUX_COLLECTION')]
        self.DEFAULT_ORE = self.DB[os.getenv('AUG_COLLECTION')]
        self.MINTS_ORES = self.DB[os.getenv('MINTS_COLLECTION')]
        
    def mongo_killer(self):
        self.CLIENT.close()

    def __del__(self):
        self.mongo_killer()
        
class MongoDBOresPile:

    def __init__(self):
        self.mongo_connection = MongoDBInitializer()

    def add_coin_to_db(self, ore, name, year, price, quantity, weight):
        row = {
               'name': name,
               'year': year,
               'price': price,
               'quantity': quantity,
               'weight[oz]': weight
               }
        if ore == 'AUG':
            self.mongo_connection.DEFAULT_ORE.insert_one(row)
        else:
            self.mongo_connection.AUX_COLLECTION.insert_one(row)
        self.mongo_connection.mongo_killer()

    def find_single_ore(self, value):
#         value format = {'key': 'value'}
        return self.mongo_connection.DEFAULT_ORE.find_one(value)

    def find_all_one_ore_sorted_by_price(self):
        return [f'{one_ore["name"]} - {float(one_ore["price"])*float(one_ore["quantity"])}'
                for one_ore in self.mongo_connection.DEFAULT_ORE.find({}).sort("price", pymongo.DESCENDING)]

    def find_all_one_ore_with_name_and_year(self):
        return [f'{one_ore["name"]} {one_ore["year"]} - {one_ore["price"]}'
                for one_ore in self.mongo_connection.DEFAULT_ORE.find({})]

    def find_all_one_ore_sorted_by_name(self):
        return [f'{one_ore["name"]}' for one_ore in self.mongo_connection.DEFAULT_ORE.find({})]

    def count_all_aug_ores_value(self):
        ores = [float(one_ore["price"])*float(one_ore["quantity"]) for one_ore in self.mongo_connection.DEFAULT_ORE.find({})]
        return sum(num for num in ores)

    def count_all_aux_ores_value(self):
        ores = [float(one_ore["price"])*float(one_ore["quantity"]) for one_ore in self.mongo_connection.AUX_COLLECTION.find({})]
        return sum(num for num in ores)
    def count_weight_of_AUG_ore(self):
        ores = [float(one_ore["quantity"])*float(one_ore["weight[oz]"]) for one_ore in self.mongo_connection.DEFAULT_ORE.find({})]
        return sum(num for num in ores)

    def count_weight_of_AUX_ore(self):
        ores = [float(one_ore["quantity"])*float(one_ore["weight[oz]"]) for one_ore in self.mongo_connection.AUX_COLLECTION.find({})]
        return sum(num for num in ores)
    def list_of_ore_weight(self):
        return [self.count_weight_of_AUG_ore(), self.count_weight_of_AUX_ore()]


    # Collections from mints #
    def find_all_stashed_ore_from_mints(self):
        return [f'{one_ore["name"]}' for one_ore in self.mongo_connection.MINTS_ORES.find({})]

    def __del__(self):
        del self.mongo_connection

class MongoDBMintsScrapper:

    def __init__(self):
        self.mongo_connection = MongoDBInitializer()

    # add ore from mint with current price and date #
    def add_document(self, ores_from_mint, mint_url, mint):

        for ore in ores_from_mint:
            match = match_engine(mint, ore.strip())
            if match:
                name, year, price = match.groups()
                load_ore = {
                    "name": name.strip(),
                    "year": int(year.strip()) if year else datetime.now().year,
                    "price": float(price.replace(',', '.').strip()),
                    'mint': mint_url,
                    'added_in': todays_date()
                }
                self.mongo_connection.MINTS_ORES.insert_one(load_ore)
        self.mongo_connection.mongo_killer()

