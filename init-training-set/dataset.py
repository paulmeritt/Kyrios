import os
import json
from core.logger import Logger
from data.data_manager import DataManager

class Dataset:
    def __init__(self):
        self.logger = Logger()
        self.data_manager = DataManager()

    def generate_initial_dataset(self, raw_data):
        """
        Generate the initial dataset for training.
        """
        try:
            if not raw_data:
                self.logger.log_warning("No raw data to generate dataset.")
                return None

            processed_data = []
            for entry in raw_data:
                processed_data.append(self._process_entry(entry))
            
            self.logger.log_info("Initial dataset generated successfully.")
            return processed_data
        except Exception as e:
            self.logger.log_error(f"Error generating dataset: {e}")
            return None

    def _process_entry(self, entry):
        """
        Process each entry to extract relevant data for training.
        """
        try:
            processed_entry = {
                'text': entry['message'],
                'timestamp': entry['timestamp'],
                'labels': self._generate_labels(entry['message'])
            }
            return processed_entry
        except Exception as e:
            self.logger.log_error(f"Error processing entry: {e}")
            return None

    def _generate_labels(self, message):
        """
        Generate labels based on the content of the message.
        """
        if "join" in message.lower():
            return 1  # Join label
        elif "follow" in message.lower():
            return 2  # Follow label
        else:
            return 0  # Neutral label

if __name__ == "__main__":
    dataset = Dataset()
    raw_data = dataset.load_data("path/to/raw_data.json")
    initial_dataset = dataset.generate_initial_dataset(raw_data)
    dataset.save_data(initial_dataset, "path/to/initial_dataset.json")
