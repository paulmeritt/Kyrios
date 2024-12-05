import logging
import os

class Logger:
    def __init__(self, log_dir="kyrios_logs", log_level=logging.INFO):
        self.log_dir = log_dir
        self.log_level = log_level
        self._setup_logger()

    def _setup_logger(self):
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)

        log_filename = os.path.join(self.log_dir, "kyrios_log.log")
        self.logger = logging.getLogger("KyriosLogger")
        self.logger.setLevel(self.log_level)

        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(self.log_level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_debug(self, message):
        self.logger.debug(message)

    def log_critical(self, message):
        self.logger.critical(message)
