import os
import sys
import logging
from datetime import datetime
from core.ai_engine import AIEngine
from core.database import Database
from core.logger import Logger
from core.utils import Utils

class FollowerManager:
    def __init__(self):
        self.logger = Logger()
        self.db = Database()
        self.ai_engine = AIEngine()

    def add_follower(self, user_id):
        try:
            timestamp = datetime.now().isoformat()
            self.ai_engine.add_follower(user_id)
            self.db.store_follower(user_id, timestamp)
            self.logger.log_info(f"Follower {user_id} added successfully.")
        except Exception as e:
            self.logger.log_error(f"Error adding follower {user_id}: {e}")

    def remove_follower(self, user_id):
        try:
            self.db.remove_follower(user_id)
            self.ai_engine.followers = [f for f in self.ai_engine.followers if f != user_id]
            self.logger.log_info(f"Follower {user_id} removed successfully.")
        except Exception as e:
            self.logger.log_error(f"Error removing follower {user_id}: {e}")

    def list_followers(self):
        try:
            followers = self.db.get_followers()
            self.logger.log_info(f"Current followers: {followers}")
            return followers
        except Exception as e:
            self.logger.log_error(f"Error listing followers: {e}")
            return []

    def run(self):
        while True:
            user_input = input("Enter a command: ")
            if user_input == "add":
                user_id = input("Enter user ID to add: ")
                self.add_follower(user_id)
            elif user_input == "remove":
                user_id = input("Enter user ID to remove: ")
                self.remove_follower(user_id)
            elif user_input == "list":
                self.list_followers()
            elif user_input == "exit":
                break
            else:
                self.logger.log_warning("Invalid command.")

if __name__ == "__main__":
    follower_manager = FollowerManager()
    follower_manager.run()
