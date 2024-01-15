from nltk.data import find
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Helpers.utils import translate_sentence
import nltk
import os

from DB.pile import MongoDBOwnPile
from Scrappers.scrapers import CoinPriceScraper

class CompareOresMachine(CoinPriceScraper, MongoDBOwnPile):

    def preprocess_text(self, text):
        # Check tokenizers library #
        try:
            find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            os.environ["TK_SILENCE_DEPRECATION"] = "1"
        # tokenize every word in sentence #
        words = word_tokenize(text)
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(word) for word in words]
        return ' '.join(stemmed_words)

    def find_similar_ore(self):
        # Using NLTK, app can match similar ores to compare prices #
        '''
        POC - work in progress
        '''

        # Working with one value checking poc. Work in progress #
        list_from_scrapper = self.mints_scrapper()[0]
        # Preprocesses the translated ore and ores obtained from the scrapper #
        ore_from_db = translate_sentence(self.find_all_one_ore_with_name_and_year()[6])

        # Uses TF-IDFto convert text into numerical vectors and measure similarity #
        preprocessed_query = self.preprocess_text(ore_from_db)
        preprocessed_ore_from_scrapper = [self.preprocess_text(ore) for ore in list_from_scrapper]
        all_ores = [preprocessed_query] + preprocessed_ore_from_scrapper

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_ores)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)[0]

        similar_indices = [i for i, score in enumerate(similarities) if score > 0.75]
        similar_sentences = [all_ores[i] for i in similar_indices]
        return similar_sentences

# CompareOresMachine().find_similar_ore()

