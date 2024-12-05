import socket
import json
import sys
from core.logger import Logger
from core.utils import Utils

class Client:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.client_socket = None
        self.logger = Logger()

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.logger.log_info(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            self.logger.log_error(f"Error connecting to server: {e}")
            sys.exit(1)

    def send_message(self, message):
        try:
            message_data = json.dumps({"action": "send_message", "message": message})
            self.client_socket.send(message_data.encode('utf-8'))
            self.logger.log_info(f"Sent message: {message}")
        except Exception as e:
            self.logger.log_error(f"Error sending message: {e}")

    def receive_response(self):
        try:
            response = self.client_socket.recv(1024)
            if response:
                data = json.loads(response.decode('utf-8'))
                self.logger.log_info(f"Received response: {data['response']}")
                return data['response']
            else:
                self.logger.log_error("No response received")
                return None
        except Exception as e:
            self.logger.log_error(f"Error receiving response: {e}")
            return None

    def close_connection(self):
        try:
            self.client_socket.close()
            self.logger.log_info("Connection closed.")
        except Exception as e:
            self.logger.log_error(f"Error closing connection: {e}")

    def run(self):
        self.connect_to_server()
        while True:
            user_input = input("Enter message to send (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            self.send_message(user_input)
            response = self.receive_response()
            print(f"Server Response: {response}")
        self.close_connection()

if __name__ == "__main__":
    client = Client()
    client.run()
