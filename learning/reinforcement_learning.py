import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from core.logger import Logger
from core.utils import Utils
from data.database import Database
from data.data_manager import DataManager

class ReinforcementLearning:
    def __init__(self):
        self.logger = Logger()
        self.db = Database()
        self.data_manager = DataManager()
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def preprocess_data(self, data):
        try:
            features = []
            rewards = []
            for entry in data:
                feature = [len(entry['message']), len(entry['timestamp']), self._get_sentiment_score(entry['message'])]
                reward = self._calculate_reward(entry['message'])
                features.append(feature)
                rewards.append(reward)

            features = np.array(features)
            rewards = np.array(rewards)
            features = self.scaler.fit_transform(features)
            return features, rewards
        except Exception as e:
            self.logger.log_error(f"Error preprocessing data: {e}")
            return None, None

    def _get_sentiment_score(self, message):
        positive_words = ["good", "happy", "joy", "positive", "great"]
        negative_words = ["bad", "sad", "anger", "negative", "poor"]
        sentiment_score = 0
        for word in positive_words:
            sentiment_score += message.lower().count(word)
        for word in negative_words:
            sentiment_score -= message.lower().count(word)
        return sentiment_score

    def _calculate_reward(self, message):
        if "join" in message.lower():
            return 1  # Positive reward for joining
        elif "leave" in message.lower():
            return -1  # Negative reward for leaving
        else:
            return 0  # Neutral reward

    def train(self, data):
        try:
            features, rewards = self.preprocess_data(data)
            if features is not None and rewards is not None:
                self.model.fit(features, rewards)
                self.logger.log_info("Reinforcement learning model trained.")
            else:
                self.logger.log_error("Training failed due to preprocessing errors.")
        except Exception as e:
            self.logger.log_error(f"Error during training: {e}")

    def update_model(self, new_data):
        try:
            self.logger.log_info("Updating reinforcement learning model...")
            features, rewards = self.preprocess_data(new_data)
            if features is not None and rewards is not None:
                self.model.fit(features, rewards)
                self.logger.log_info("Model updated successfully.")
            else:
                self.logger.log_error("Failed to update model. Invalid data.")
        except Exception as e:
            self.logger.log_error(f"Error updating model: {e}")

    def predict(self, message):
        try:
            feature = np.array([[len(message), len(message), self._get_sentiment_score(message)]])
            feature = self.scaler.transform(feature)
            reward = self.model.predict(feature)
            self.logger.log_info(f"Predicted reward: {reward[0]}")
            return reward[0]
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
        while True:
            data = self.db.get_interactions("user1")  # Example user
            if data:
                self.update_model(data)
            else:
                self.logger.log_warning("No data found for learning.")
            sleep(3600)

if __name__ == "__main__":
    reinforcement_learning = ReinforcementLearning()
    reinforcement_learning.run()
