import socket
import threading
import json
from core.logger import Logger
from core.utils import Utils

class PeerToPeer:
    def __init__(self, host='127.0.0.1', port=5001):
        self.host = host
        self.port = port
        self.peer_socket = None
        self.logger = Logger()
        self.connections = {}

    def start_peer_server(self):
        try:
            self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.peer_socket.bind((self.host, self.port))
            self.peer_socket.listen(5)
            self.logger.log_info(f"Peer-to-peer server started at {self.host}:{self.port}")
            self.accept_peer_connections()
        except Exception as e:
            self.logger.log_error(f"Error starting peer server: {e}")

    def accept_peer_connections(self):
        try:
            while True:
                peer_socket, peer_address = self.peer_socket.accept()
                self.connections[peer_address] = peer_socket
                self.logger.log_info(f"New peer connection from {peer_address}")
                peer_handler = threading.Thread(target=self.handle_peer, args=(peer_socket, peer_address))
                peer_handler.start()
        except Exception as e:
            self.logger.log_error(f"Error accepting peer connections: {e}")

    def handle_peer(self, peer_socket, peer_address):
        try:
            while True:
                request = peer_socket.recv(1024)
                if not request:
                    break
                message = request.decode('utf-8')
                self.logger.log_info(f"Received peer message: {message}")
                self.process_peer_message(peer_socket, peer_address, message)
        except Exception as e:
            self.logger.log_error(f"Error handling peer {peer_address}: {e}")
        finally:
            self.logger.log_info(f"Closing connection with {peer_address}")
            peer_socket.close()
            del self.connections[peer_address]

    def process_peer_message(self, peer_socket, peer_address, message):
        try:
            data = json.loads(message)
            if "action" in data:
                if data["action"] == "send_message":
                    self.send_peer_message(peer_socket, peer_address, data.get("message", ""))
                else:
                    self.logger.log_warning(f"Unknown peer action: {data['action']}")
            else:
                self.logger.log_warning("Invalid message structure")
        except Exception as e:
            self.logger.log_error(f"Error processing peer message: {e}")

    def send_peer_message(self, peer_socket, peer_address, message):
        try:
            response = json.dumps({"response": message})
            peer_socket.send(response.encode('utf-8'))
            self.logger.log_info(f"Sent response to peer {peer_address}: {message}")
        except Exception as e:
            self.logger.log_error(f"Error sending message to peer {peer_address}: {e}")

    def shutdown_peer_server(self):
        try:
            self.peer_socket.close()
            self.logger.log_info("Peer-to-peer server shut down successfully.")
        except Exception as e:
            self.logger.log_error(f"Error shutting down peer server: {e}")

if __name__ == "__main__":
    peer_server = PeerToPeer()
    peer_server.start_peer_server()
