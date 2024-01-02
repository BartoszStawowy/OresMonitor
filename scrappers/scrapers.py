from bs4 import BeautifulSoup
from guideposts import guidepost
from helpers.utils import encode, eliminate_redundant_words, translate_sentence
from DB.pile import MongoDBOwnPile, MongoDBMintsScrapper
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import os


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

            MongoDBMintsScrapper().add_document(eliminate_redundant_words(coins_list), data_package['main_url'], data_package['mint'])

        else:
            print(f'Website is response with code {response.status_code}.')

    def mints_scrapper(self):
        return [self.check_resposne_and_parse(guidepost.load_json_package(mint)) for mint in self.mints]


class CompareOresMachine(CoinPriceScraper, MongoDBOwnPile):

    def preprocess_text(self, text):
        # nltk.download_shell()
        os.environ["TK_SILENCE_DEPRECATION"] = "1"
        words = word_tokenize(text)
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(word) for word in words]
        return ' '.join(stemmed_words)

    def find_similar_ore(self):
        list_from_scrapper = self.mints_scrapper()[0]
        ore_from_db = translate_sentence(self.find_all_one_ore_with_name_and_year()[7])

        preprocessed_query = self.preprocess_text(ore_from_db)
        preprocessed_ore_from_scrapper = [self.preprocess_text(ore) for ore in list_from_scrapper]
        all_ores = [preprocessed_query] + preprocessed_ore_from_scrapper

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_ores)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)[0]

        similar_indices = [i for i, score in enumerate(similarities) if score > 0.55]
        similar_sentences = [all_ores[i] for i in similar_indices]
        return similar_sentences

CompareOresMachine().find_similar_ore()