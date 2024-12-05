import hashlib
import os
from core.logger import Logger

class Security:
    def __init__(self):
        self.logger = Logger()

    def generate_hash(self, data):
        """
        Generate a secure hash for the provided data.
        """
        try:
            hash_object = hashlib.sha256(data.encode('utf-8'))
            return hash_object.hexdigest()
        except Exception as e:
            self.logger.log_error(f"Error generating hash: {e}")
            return None

    def verify_hash(self, data, expected_hash):
        """
        Verify if the provided data matches the expected hash.
        """
        try:
            generated_hash = self.generate_hash(data)
            if generated_hash == expected_hash:
                self.logger.log_info("Hash verification successful.")
                return True
            else:
                self.logger.log_warning("Hash verification failed.")
                return False
        except Exception as e:
            self.logger.log_error(f"Error verifying hash: {e}")
            return False

    def encrypt_data(self, data, key):
        """
        Encrypt the data using a symmetric encryption algorithm (AES).
        """
        try:
            from Crypto.Cipher import AES
            cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
            return cipher.nonce + tag + ciphertext
        except Exception as e:
            self.logger.log_error(f"Error encrypting data: {e}")
            return None

    def decrypt_data(self, encrypted_data, key):
        """
        Decrypt the data using the provided key.
        """
        try:
            from Crypto.Cipher import AES
            nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
            cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX, nonce=nonce)
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            self.logger.log_error(f"Error decrypting data: {e}")
            return None

if __name__ == "__main__":
    security = Security()
    data = "Sensitive data"
    key = "secret_key_123"
    encrypted_data = security.encrypt_data(data, key)
    decrypted_data = security.decrypt_data(encrypted_data, key)
    print(f"Decrypted Data: {decrypted_data}")
