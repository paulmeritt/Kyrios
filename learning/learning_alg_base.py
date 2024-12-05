import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from core.logger import Logger
from core.utils import Utils
from data.database import Database
from data.data_manager import DataManager

class LearningAlgorithm:
    def __init__(self):
        self.logger = Logger()
        self.db = Database()
        self.data_manager = DataManager()
        self.scaler = StandardScaler()
        self.model = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=500, solver='adam')

    def preprocess_data(self, data):
        try:
            features = []
            labels = []
            for entry in data:
                feature = [len(entry['message']), len(entry['timestamp']), self._get_sentiment_score(entry['message'])]
                label = self._get_label_from_message(entry['message'])
                features.append(feature)
                labels.append(label)

            features = np.array(features)
            labels = np.array(labels)
            features = self.scaler.fit_transform(features)
            return features, labels
        except Exception as e:
            self.logger.log_error(f"Error preprocessing data: {e}")
            return None, None

    def _get_sentiment_score(self, message):
        """
        Placeholder function to calculate sentiment score. Can be replaced with an NLP model.
        """
        positive_words = ["good", "happy", "joy", "positive", "great"]
        negative_words = ["bad", "sad", "anger", "negative", "poor"]
        sentiment_score = 0
        for word in positive_words:
            sentiment_score += message.lower().count(word)
        for word in negative_words:
            sentiment_score -= message.lower().count(word)
        return sentiment_score

    def _get_label_from_message(self, message):
        """
        Placeholder for determining message intent. Can be customized for Kyrios' interaction patterns.
        """
        if "join" in message.lower():
            return 1
        elif "follow" in message.lower():
            return 2
        else:
            return 0

    def train(self, data):
        try:
            features, labels = self.preprocess_data(data)
            if features is not None and labels is not None:
                X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)
                self.model.fit(X_train, y_train)
                predictions = self.model.predict(X_test)
                accuracy = accuracy_score(y_test, predictions)
                self.logger.log_info(f"Training completed with accuracy: {accuracy:.4f}")
                self.logger.log_info(f"Classification Report:\n{classification_report(y_test, predictions)}")
            else:
                self.logger.log_error("Training failed due to preprocessing errors.")
        except Exception as e:
            self.logger.log_error(f"Error during training: {e}")

    def update_model(self, new_data):
        try:
            self.logger.log_info("Updating model with new data...")
            features, labels = self.preprocess_data(new_data)
            if features is not None and labels is not None:
                self.model.partial_fit(features, labels, classes=np.unique(labels))
                self.logger.log_info("Model updated successfully.")
            else:
                self.logger.log_error("Failed to update model. Invalid data.")
        except Exception as e:
            self.logger.log_error(f"Error updating model: {e}")

    def predict(self, message):
        try:
            feature = np.array([[len(message), len(message), self._get_sentiment_score(message)]])
            feature = self.scaler.transform(feature)
            prediction = self.model.predict(feature)
            self.logger.log_info(f"Predicted label: {prediction[0]}")
            return prediction[0]
        except Exception as e:
            self.logger.log_error(f"Error during prediction: {e}")
            return None

    def save_model(self, file_path):
        try:
            from joblib import dump
            dump(self.model, file_path)
            self.logger.log_info(f"Model saved to {file_path}")
        except Exception as e:
            self.logger.log_error(f"Error saving model: {e}")

    def load_model(self, file_path):
        try:
            from joblib import load
            self.model = load(file_path)
            self.logger.log_info(f"Model loaded from {file_path}")
        except Exception as e:
            self.logger.log_error(f"Error loading model: {e}")

    def run(self):
        """
        Continuous learning loop for Kyrios to improve.
        """
        while True:
            data = self.db.get_interactions("user1")  # Example user
            if data:
                self.update_model(data)
            else:
                self.logger.log_warning("No data found for learning.")
            sleep(3600)  # Run every hour to update model

if __name__ == "__main__":
    learning_algorithm = LearningAlgorithm()
    learning_algorithm.run()
