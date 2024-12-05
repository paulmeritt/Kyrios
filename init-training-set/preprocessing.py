import re
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from core.logger import Logger
from data.data_manager import DataManager

nltk.download('stopwords')
from nltk.corpus import stopwords

class Preprocessing:
    def __init__(self):
        self.logger = Logger()
        self.data_manager = DataManager()
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, raw_text):
        """
        Basic preprocessing steps: Lowercasing, removing punctuation, stopwords, and stemming.
        """
        try:
            text = raw_text.lower()
            text = self._remove_punctuation(text)
            text = self._remove_stopwords(text)
            text = self._apply_stemming(text)
            return text
        except Exception as e:
            self.logger.log_error(f"Error in text preprocessing: {e}")
            return ""

    def _remove_punctuation(self, text):
        """
        Remove punctuation from the text.
        """
        return text.translate(str.maketrans('', '', string.punctuation))

    def _remove_stopwords(self, text):
        """
        Remove stopwords from the text.
        """
        return ' '.join([word for word in text.split() if word not in self.stop_words])

    def _apply_stemming(self, text):
        """
        Apply stemming to the words in the text.
        """
        from nltk.stem import PorterStemmer
        ps = PorterStemmer()
        return ' '.join([ps.stem(word) for word in text.split()])

    def extract_features(self, data):
        """
        Extract TF-IDF features from the preprocessed text data.
        """
        try:
            vectorizer = TfidfVectorizer()
            features = vectorizer.fit_transform(data)
            self.logger.log_info("Features extracted using TF-IDF.")
            return features
        except Exception as e:
            self.logger.log_error(f"Error in feature extraction: {e}")
            return None

if __name__ == "__main__":
    preprocessing = Preprocessing()
    raw_texts = ["This is a sample text.", "Kyrios will lead us."]
    processed_texts = [preprocessing.preprocess_text(text) for text in raw_texts]
    features = preprocessing.extract_features(processed_texts)
