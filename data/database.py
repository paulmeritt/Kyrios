import sqlite3
import json
from core.logger import Logger
from core.config import Config

class Database:
    def __init__(self, db_name=Config.DATABASE_NAME):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.logger = Logger()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.logger.log_info(f"Connected to database {self.db_name}")
        except Exception as e:
            self.logger.log_error(f"Error connecting to database: {e}")
            raise

    def close(self):
        try:
            if self.connection:
                self.connection.commit()
                self.connection.close()
                self.logger.log_info("Database connection closed.")
        except Exception as e:
            self.logger.log_error(f"Error closing database connection: {e}")

    def create_table(self):
        try:
            self.connect()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            self.logger.log_info("Interactions table created or already exists.")
        except Exception as e:
            self.logger.log_error(f"Error creating table: {e}")
        finally:
            self.close()

    def store_interaction(self, user_id, message, timestamp):
        try:
            self.connect()
            self.cursor.execute("""
                INSERT INTO interactions (user_id, message, timestamp)
                VALUES (?, ?, ?)
            """, (user_id, message, timestamp))
            self.logger.log_info(f"Interaction stored for user {user_id}")
        except Exception as e:
            self.logger.log_error(f"Error storing interaction: {e}")
        finally:
            self.close()

    def get_interactions(self, user_id):
        try:
            self.connect()
            self.cursor.execute("""
                SELECT message, timestamp FROM interactions
                WHERE user_id = ?
            """, (user_id,))
            interactions = self.cursor.fetchall()
            self.logger.log_info(f"Retrieved {len(interactions)} interactions for user {user_id}")
            return interactions
        except Exception as e:
            self.logger.log_error(f"Error retrieving interactions: {e}")
            return []
        finally:
            self.close()

    def store_follower(self, user_id, timestamp):
        try:
            self.connect()
            self.cursor.execute("""
                INSERT INTO followers (user_id, timestamp)
                VALUES (?, ?)
            """, (user_id, timestamp))
            self.logger.log_info(f"Follower {user_id} added.")
        except Exception as e:
            self.logger.log_error(f"Error storing follower {user_id}: {e}")
        finally:
            self.close()

    def get_followers(self):
        try:
            self.connect()
            self.cursor.execute("SELECT user_id FROM followers")
            followers = self.cursor.fetchall()
            self.logger.log_info(f"Retrieved {len(followers)} followers.")
            return [f[0] for f in followers]
        except Exception as e:
            self.logger.log_error(f"Error retrieving followers: {e}")
            return []
        finally:
            self.close()
