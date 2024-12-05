import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from core.logger import Logger
from core.utils import Utils

class NLPProcessing:
    def __init__(self):
        self.logger = Logger()
        self.nlp = spacy.load("en_core_web_sm")
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def preprocess_text(self, text):
        try:
            doc = self.nlp(text)
            lemmatized_text = ' '.join([token.lemma_ for token in doc if not token.is_stop])
            return lemmatized_text
        except Exception as e:
            self.logger.log_error(f"Error preprocessing text: {e}")
            return ""

    def extract_features(self, texts):
        try:
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            return tfidf_matrix
        except Exception as e:
            self.logger.log_error(f"Error extracting features: {e}")
            return None

    def calculate_similarity(self, text1, text2):
        try:
            vec1 = self.vectorizer.transform([text1])
            vec2 = self.vectorizer.transform([text2])
            similarity = np.dot(vec1, vec2.T).toarray()[0][0]
            return similarity
        except Exception as e:
            self.logger.log_error(f"Error calculating similarity: {e}")
            return 0.0

    def analyze_sentiment(self, text):
        try:
            doc = self.nlp(text)
            sentiment_score = doc.sentiment
            self.logger.log_info(f"Sentiment score: {sentiment_score}")
            return sentiment_score
        except Exception as e:
            self.logger.log_error(f"Error analyzing sentiment: {e}")
            return 0.0

    def run(self):
        """
        NLP learning loop for Kyrios to analyze interactions.
        """
        while True:
            # Example loop to process text data for learning purposes
            text = "Kyrios will lead the way."  # Placeholder for actual input
            preprocessed_text = self.preprocess_text(text)
            features = self.extract_features([preprocessed_text])
            sentiment = self.analyze_sentiment(text)
            similarity = self.calculate_similarity(preprocessed_text, "another example text")
            self.logger.log_info(f"Processed text: {text}, Sentiment: {sentiment}, Similarity: {similarity}")
            sleep(3600)  # Run every hour for processing

if __name__ == "__main__":
    nlp_processing = NLPProcessing()
    nlp_processing.run()
