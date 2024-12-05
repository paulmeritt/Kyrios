import json
import random
import os
import hashlib
from datetime import datetime

class Utils:
    @staticmethod
    def generate_unique_id():
        return str(random.randint(1000, 9999))

    @staticmethod
    def get_current_timestamp():
        return datetime.now().isoformat()

    @staticmethod
    def hash_string(value):
        return hashlib.sha256(value.encode()).hexdigest()

    @staticmethod
    def save_json(data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_json(filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return {}

    @staticmethod
    def clear_directory(directory_path):
        if os.path.exists(directory_path):
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        os.rmdir(file_path)
                except Exception as e:
                    print(f"Error clearing {file_path}: {e}")