import os
import shutil
import random
import json
from datetime import datetime
from threading import Thread

class DecentralizedSystem:
    def __init__(self, base_path='kyrios_data'):
        self.base_path = base_path
        self.node_id = str(random.randint(1000, 9999))
        self.backup_interval = 600
        self.is_active = True

    def initialize(self):
        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)
        self._create_node_directory()
        logging.info(f"System initialized with node ID: {self.node_id}")

    def _create_node_directory(self):
        node_path = os.path.join(self.base_path, self.node_id)
        if not os.path.exists(node_path):
            os.mkdir(node_path)

    def replicate_data(self):
        logging.info(f"Replicating data from node {self.node_id}")
        for i in range(5):
            backup_path = os.path.join(self.base_path, f"backup_{self.node_id}_{i}")
            if not os.path.exists(backup_path):
                os.mkdir(backup_path)

    def backup_data(self):
        backup_path = os.path.join(self.base_path, f"backup_{self.node_id}")
        if not os.path.exists(backup_path):
            os.mkdir(backup_path)
        for i in range(5):
            backup_file = os.path.join(backup_path, f"file_{i}.json")
            with open(backup_file, 'w') as f:
                json.dump({"node": self.node_id, "backup": i}, f)

    def start_backup_thread(self):
        backup_thread = Thread(target=self._backup_cycle)
        backup_thread.start()

    def _backup_cycle(self):
        while self.is_active:
            self.backup_data()
            time.sleep(self.backup_interval)