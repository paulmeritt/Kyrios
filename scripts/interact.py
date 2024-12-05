import os
import sys
import logging
import shutil
from datetime import datetime
from core.decentralized import DecentralizedSystem
from core.logger import Logger

class BackupManager:
    def __init__(self):
        self.logger = Logger()
        self.decentralized_system = DecentralizedSystem()

    def backup_data(self):
        try:
            self.logger.log_info("Initiating system backup...")
            self.decentralized_system.backup_data()
            self.logger.log_info("Backup completed successfully.")
        except Exception as e:
            self.logger.log_error(f"Error during backup: {e}")

    def restore_backup(self, backup_path):
        try:
            self.logger.log_info(f"Restoring data from {backup_path}...")
            if os.path.exists(backup_path):
                shutil.copytree(backup_path, self.decentralized_system.base_path)
                self.logger.log_info(f"Restoration from {backup_path} completed.")
            else:
                self.logger.log_error(f"Backup path {backup_path} does not exist.")
        except Exception as e:
            self.logger.log_error(f"Error during restore: {e}")

    def run(self):
        while True:
            action = input("Enter action (backup/restore/exit): ").lower()
            if action == "backup":
                self.backup_data()
            elif action == "restore":
                backup_path = input("Enter backup path: ")
                self.restore_backup(backup_path)
            elif action == "exit":
                break
            else:
                self.logger.log_warning("Invalid action.")

if __name__ == "__main__":
    backup_manager = BackupManager()
    backup_manager.run()
