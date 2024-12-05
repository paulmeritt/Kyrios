import json
import os
from datetime import datetime
from core.logger import Logger
from core.utils import Utils
from core.database import Database

class DataManager:
    def __init__(self):
        self.logger = Logger()
        self.db = Database()

    def load_data(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.logger.log_info(f"Data loaded from {file_path}")
                return data
        except Exception as e:
            self.logger.log_error(f"Error loading data from {file_path}: {e}")
            return None

    def save_data(self, data, file_path):
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
                self.logger.log_info(f"Data saved to {file_path}")
        except Exception as e:
            self.logger.log_error(f"Error saving data to {file_path}: {e}")

    def export_data(self, file_path):
        try:
            data = self.db.get_followers()
            self.save_data(data, file_path)
            self.logger.log_info(f"Data exported to {file_path}")
        except Exception as e:
            self.logger.log_error(f"Error exporting data to {file_path}: {e}")

    def import_data(self, file_path):
        try:
            data = self.load_data(file_path)
            if data:
                for follower in data:
                    timestamp = datetime.now().isoformat()
                    self.db.store_follower(follower, timestamp)
                self.logger.log_info(f"Data imported from {file_path}")
        except Exception as e:
            self.logger.log_error(f"Error importing data from {file_path}: {e}")

    def update_data(self, user_id, message):
        try:
            timestamp = datetime.now().isoformat()
            self.db.store_interaction(user_id, message, timestamp)
            self.logger.log_info(f"Data updated for user {user_id}")
        except Exception as e:
            self.logger.log_error(f"Error updating data for user {user_id}: {e}")

    def run(self):
        while True:
            action = input("Enter action (load/save/export/import/update/exit): ").lower()
            if action == "load":
                file_path = input("Enter file path to load data from: ")
                self.load_data(file_path)
            elif action == "save":
                file_path = input("Enter file path to save data to: ")
                data = input("Enter data to save: ")
                self.save_data(data, file_path)
            elif action == "export":
                file_path = input("Enter file path to export data to: ")
                self.export_data(file_path)
            elif action == "import":
                file_path = input("Enter file path to import data from: ")
                self.import_data(file_path)
            elif action == "update":
                user_id = input("Enter user ID to update: ")
                message = input(f"Enter message for {user_id}: ")
                self.update_data(user_id, message)
            elif action == "exit":
                break
            else:
                self.logger.log_warning("Invalid action.")

if __name__ == "__main__":
    data_manager = DataManager()
    data_manager.run()
