import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from core.logger import Logger
from data.data_manager import DataManager
from init_training_set.preprocessing import Preprocessing
from init_training_set.data_loader import DataLoader

class TrainingPipeline:
    def __init__(self):
        self.logger = Logger()
        self.data_loader = DataLoader()
        self.preprocessing = Preprocessing()
        self.data_manager = DataManager()

    def train_model(self, training_data):
        """
        Train the model using the preprocessed data.
        """
        try:
            features, labels = self._prepare_data(training_data)
            if features is None or labels is None:
                self.logger.log_warning("No data available for training.")
                return None

            X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)
            model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, solver='adam')
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)

            self.logger.log_info(f"Model trained with accuracy: {accuracy:.4f}")
            return model
        except Exception as e:
            self.logger.log_error(f"Error during model training: {e}")
            return None

    def _prepare_data(self, data):
        """
        Process and extract features and labels from the raw data.
        """
        try:
            labels = data['labels'].values
            features = self.preprocessing.extract_features(data['text'])
            return features, labels
        except Exception as e:
            self.logger.log_error(f"Error preparing data: {e}")
            return None, None

    def save_model(self, model, file_path):
        """
        Save the trained model.
        """
        try:
            from joblib import dump
            dump(model, file_path)
            self.logger.log_info(f"Model saved to {file_path}")
        except Exception as e:
            self.logger.log_error(f"Error saving model: {e}")

if __name__ == "__main__":
    training_pipeline = TrainingPipeline()
    raw_data = training_pipeline.data_loader.load_data("path/to/processed_data.json")
    model = training_pipeline.train_model(raw_data)
    if model:
        training_pipeline.save_model(model, "path/to/saved_model.joblib")
