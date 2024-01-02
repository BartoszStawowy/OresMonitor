from bs4 import BeautifulSoup
from Guideposts import guidepost
from Helpers.utils import encode, eliminate_redundant_words, translate_sentence
from DB.pile import MongoDBMintsScrapper
import requests



class CoinPriceScraper:
    mints = ['dragon_mint', 'silver_mint']


    def check_resposne_and_parse(self, data_package):
        response = requests.get(f"{data_package['main_url']}{data_package['silver_suffix']}")
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            coins_header = soup.find_all(f"{data_package['coins_header']}", class_=f"{data_package['coins_header_class']}")
            coin_names = [link.a.get_text(strip=True) for link in coins_header]

            coins_price = soup.find_all(f"{data_package['coins_price']}", class_=f"{data_package['coins_price_class']}")
            coin_prices = [price.get_text(strip=True) for price in coins_price]

            coins_list = [f"{name} - {price}" for name, price in zip(coin_names, coin_prices)]

            MongoDBMintsScrapper().add_document(eliminate_redundant_words(encode(coins_list)), data_package['main_url'], data_package['mint'])

        else:
            print(f'Website is response with code {response.status_code}.')

    def mints_scrapper(self):
        return [self.check_resposne_and_parse(guidepost.load_json_package(mint)) for mint in self.mints]



