import json
import os
from core.logger import Logger

class DataUtils:
    def __init__(self):
        self.logger = Logger()

    def validate_data(self, data, schema):
        """
        Validate data against a predefined schema.
        """
        try:
            for key in schema:
                if key not in data:
                    self.logger.log_warning(f"Missing key: {key}")
                    return False
            self.logger.log_info("Data validation successful.")
            return True
        except Exception as e:
            self.logger.log_error(f"Error validating data: {e}")
            return False

    def process_data(self, data):
        """
        Process data by performing transformations.
        """
        try:
            if isinstance(data, list):
                processed_data = [self.transform(item) for item in data]
            else:
                processed_data = self.transform(data)
            self.logger.log_info(f"Data processed successfully.")
            return processed_data
        except Exception as e:
            self.logger.log_error(f"Error processing data: {e}")
            return None

    def transform(self, data):
        """
        Transform individual data item.
        """
        try:
            if isinstance(data, dict):
                transformed_data = {key.upper(): value for key, value in data.items()}
            else:
                transformed_data = data
            return transformed_data
        except Exception as e:
            self.logger.log_error(f"Error transforming data: {e}")
            return None

    def store_data(self, data, file_path):
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            self.logger.log_info(f"Data saved to {file_path}")
        except Exception as e:
            self.logger.log_error(f"Error storing data to {file_path}: {e}")

    def load_data(self, file_path):
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.logger.log_info(f"Data loaded from {file_path}")
                    return data
            else:
                self.logger.log_warning(f"File {file_path} not found.")
                return None
        except Exception as e:
            self.logger.log_error(f"Error loading data from {file_path}: {e}")
            return None
