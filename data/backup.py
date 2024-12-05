import os
import shutil
from datetime import datetime
from core.logger import Logger
from core.utils import Utils

class BackupData:
    def __init__(self, backup_directory="backups"):
        self.backup_directory = backup_directory
        self.logger = Logger()

    def backup(self, source_dir, backup_name=None):
        try:
            if not os.path.exists(self.backup_directory):
                os.makedirs(self.backup_directory)
            
            if not backup_name:
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            backup_path = os.path.join(self.backup_directory, backup_name)
            shutil.copytree(source_dir, backup_path)
            self.logger.log_info(f"Backup completed for {source_dir} to {backup_path}")
        except Exception as e:
            self.logger.log_error(f"Error during backup: {e}")

    def restore(self, backup_name, restore_dir):
        try:
            backup_path = os.path.join(self.backup_directory, backup_name)
            if os.path.exists(backup_path):
                shutil.copytree(backup_path, restore_dir)
                self.logger.log_info(f"Restored data from {backup_path} to {restore_dir}")
            else:
                self.logger.log_warning(f"Backup {backup_name} does not exist.")
        except Exception as e:
            self.logger.log_error(f"Error restoring data: {e}")

    def list_backups(self):
        try:
            backups = os.listdir(self.backup_directory)
            if backups:
                self.logger.log_info(f"Existing backups: {', '.join(backups)}")
            else:
                self.logger.log_warning("No backups found.")
            return backups
        except Exception as e:
            self.logger.log_error(f"Error listing backups: {e}")
            return []

    def delete_backup(self, backup_name):
        try:
            backup_path = os.path.join(self.backup_directory, backup_name)
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
                self.logger.log_info(f"Deleted backup {backup_name}")
            else:
                self.logger.log_warning(f"Backup {backup_name} not found.")
        except Exception as e:
            self.logger.log_error(f"Error deleting backup {backup_name}: {e}")

    def run(self):
        while True:
            action = input("Enter action (backup/restore/list/delete/exit): ").lower()
            if action == "backup":
                source_dir = input("Enter source directory to backup: ")
                self.backup(source_dir)
            elif action == "restore":
                backup_name = input("Enter backup name to restore: ")
                restore_dir = input("Enter restore directory: ")
                self.restore(backup_name, restore_dir)
            elif action == "list":
                self.list_backups()
            elif action == "delete":
                backup_name = input("Enter backup name to delete: ")
                self.delete_backup(backup_name)
            elif action == "exit":
                break
            else:
                self.logger.log_warning("Invalid action.")

if __name__ == "__main__":
    backup_data = BackupData()
    backup_data.run()
