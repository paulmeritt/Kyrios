import socket
import threading
import json
from core.logger import Logger
from core.utils import Utils
from core.config import Config

class NetworkManager:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.logger = Logger()
        self.connections = []

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.logger.log_info(f"Server started at {self.host}:{self.port}")
            self.accept_connections()
        except Exception as e:
            self.logger.log_error(f"Error starting server: {e}")

    def accept_connections(self):
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                self.connections.append(client_socket)
                self.logger.log_info(f"New connection from {client_address}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
        except Exception as e:
            self.logger.log_error(f"Error accepting connections: {e}")

    def handle_client(self, client_socket):
        try:
            while True:
                request = client_socket.recv(1024)
                if not request:
                    break
                message = request.decode('utf-8')
                self.logger.log_info(f"Received message: {message}")
                self.process_message(client_socket, message)
        except Exception as e:
            self.logger.log_error(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def process_message(self, client_socket, message):
        try:
            data = json.loads(message)
            if "action" in data:
                if data["action"] == "send_message":
                    self.send_message(client_socket, data.get("message", ""))
                else:
                    self.logger.log_warning(f"Unknown action: {data['action']}")
            else:
                self.logger.log_warning("Invalid message structure")
        except Exception as e:
            self.logger.log_error(f"Error processing message: {e}")

    def send_message(self, client_socket, message):
        try:
            response = json.dumps({"response": message})
            client_socket.send(response.encode('utf-8'))
            self.logger.log_info(f"Sent response: {message}")
        except Exception as e:
            self.logger.log_error(f"Error sending message: {e}")

    def shutdown_server(self):
        try:
            self.server_socket.close()
            self.logger.log_info("Server shut down successfully.")
        except Exception as e:
            self.logger.log_error(f"Error shutting down server: {e}")

if __name__ == "__main__":
    manager = NetworkManager()
    manager.start_server()





