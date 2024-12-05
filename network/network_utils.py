import socket
import json
import os
from core.logger import Logger
from core.utils import Utils

class NetworkUtils:
    def __init__(self):
        self.logger = Logger()

    def ping_host(self, host):
        try:
            response = os.system(f"ping -c 1 {host}")
            if response == 0:
                self.logger.log_info(f"{host} is reachable.")
                return True
            else:
                self.logger.log_warning(f"{host} is not reachable.")
                return False
        except Exception as e:
            self.logger.log_error(f"Error pinging host {host}: {e}")
            return False

    def get_network_info(self):
        try:
            host = socket.gethostname()
            ip_address = socket.gethostbyname(host)
            self.logger.log_info(f"Host: {host}, IP: {ip_address}")
            return host, ip_address
        except Exception as e:
