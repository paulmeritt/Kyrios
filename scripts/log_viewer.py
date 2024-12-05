import os
import sys
import logging
from datetime import datetime

class LogViewer:
    def __init__(self, log_dir="kyrios_logs"):
        self.log_dir = log_dir

    def view_logs(self):
        try:
            log_files = os.listdir(self.log_dir)
            log_files.sort()
            for file in log_files:
                file_path = os.path.join(self.log_dir, file)
                with open(file_path, "r") as f:
                    print(f.read())
        except Exception as e:
            logging.error(f"Error viewing logs: {e}")

    def search_logs(self, search_term):
        try:
            log_files = os.listdir(self.log_dir)
            log_files.sort()
            for file in log_files:
                file_path = os.path.join(self.log_dir, file)
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        if search_term in line:
                            print(line)
        except Exception as e:
            logging.error(f"Error searching logs: {e}")

    def run(self):
        while True:
            action = input("Enter action (view/search/exit): ").lower()
            if action == "view":
                self.view_logs()
            elif action == "search":
                search_term = input("Enter search term: ")
                self.search_logs(search_term)
            elif action == "exit":
                break
            else:
                logging.warning("Invalid action.")

if __name__ == "__main__":
    log_viewer = LogViewer()
    log_viewer.run()
