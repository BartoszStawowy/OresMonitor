from nltk.data import find
from nltk.tokenize import word_tokenize
from nltk.metrics import jaccard_distance
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from DB.pile import MongoDBOresPile
import nltk
import os

'   ------   POC   -------   '
class CompareOresMachine(MongoDBOresPile):

    def preprocess(self, text):
        # Check tokenizers library #
        try:
            find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            os.environ["TK_SILENCE_DEPRECATION"] = "1"

        # tokenize every word in sentence #
        stemmer = PorterStemmer()
        tokens = word_tokenize(text.lower())
        stemmed_tokens = [stemmer.stem(word) for word in tokens if word.isalnum()]
        return stemmed_tokens

    # verifying jaccard library #
    def jaccard_similarity(self, set1, set2):
        return 1 - jaccard_distance(set(set1), set(set2))

    def find_similar_elements(self, threshold=0.5):
        ore_from_db = self.find_all_one_ore_sorted_by_name()
        list_from_scrapper = self.find_all_stashed_ore_from_mints()

        similar_elements = []

        for my_ore in ore_from_db:
            for mint_ore in list_from_scrapper:
                tokens1 = self.preprocess(my_ore)
                tokens2 = self.preprocess(mint_ore)
                similarity = self.jaccard_similarity(tokens1, tokens2)
                if similarity >= threshold:
                    similar_elements.append((my_ore, mint_ore, similarity))
        return similar_elements

    def find_similar_elements_crosscheck(self):
        # verifying crosscheck #

        list_from_scrapper = self.find_all_stashed_ore_from_mints()
        ore_from_db = self.find_all_one_ore_sorted_by_name()
        # Using NLTK, app can match similar ores to compare prices #
        # Using TF-IDFto convert text into numerical vectors and measure similarity #
        preprocessed_query = self.preprocess(ore_from_db)
        preprocessed_ore_from_scrapper = [self.preprocess(ore) for ore in list_from_scrapper]
        all_ores = [preprocessed_query] + preprocessed_ore_from_scrapper

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_ores)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)[0]

        similar_indices = [i for i, score in enumerate(similarities) if score > 0.75]
        similar_sentences = [all_ores[i] for i in similar_indices]
        return similar_sentences

