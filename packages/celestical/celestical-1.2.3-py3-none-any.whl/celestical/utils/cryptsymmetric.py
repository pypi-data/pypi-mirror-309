import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from pathlib import Path

from celestical.compose import Compose

def _create_secret_key(self):
    # Create the secret Key
    key = os.urandom(32)
    return key

class CryptSymmetric:
    """ Class for the Encryption and decryption
    """
    
    def __init__(self, 
                 secret_key:bytes,
                 init_vector:bytes,
                 encrypt_bytes:int = 128,
                 compose:Compose = None,
                 ) -> None:
        """ Initiate with secret_key and init_vector """
        if compose is None:
            self.compose = Compose()
        self.secret_key = secret_key
        self.init_vector = init_vector
        self.encrypt_bytes = encrypt_bytes

    def _get_cipher(self) -> Cipher:
        """ Get the cipher object from cryptography"""
        crypto_algorithms = algorithms.AES(self.secret_key)

        vector = modes.CBC(self.init_vector)

        cipher = Cipher(crypto_algorithms, vector, backend=default_backend())

        return cipher

    def decryption_of_data(self, 
                           encrypted_data: str):
        """ Decryption of data with the secret key given"""
        cipher = self._get_cipher()
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        unpadder = padding.PKCS7(self.encrypt_bytes).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        decrypted_message = decrypted_data.decode('utf-8')

        return decrypted_message

    def encryption_of_data(self,
                           data: str,        
                           ):
        """ Encryption data with the secret key and self.init_vector"""

        plaintext_bytes = data.encode('utf-8')

        padder = padding.PKCS7(self.encrypt_bytes).padder()
        padded_data = padder.update(plaintext_bytes) + padder.finalize()
        cipher = self._get_cipher()

        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return ciphertext

    def encrypt_docker_compose_secrets(self, docker_compose_path:str) -> dict:
        """ Encryption of the secrets in docker compose value """
        all_encrypted_data = {}

        all_secrets = self.compose.read_all_secrets_from_compose(docker_compose_path)
        docker_compose_path = Path(docker_compose_path).resolve().parent

        for secret, file_path in all_secrets.items():
            file_path = (docker_compose_path / file_path).resolve()
            if not file_path.is_file():
                print("No File available Please check the path ", file_path.resolve())
                continue

            suffix = file_path.suffix
            if suffix in [".txt", ".json"]:
                with file_path.open('r') as file:
                    content = file.read()
                encrypted_data = self.encryption_of_data(data=content)
                all_encrypted_data[secret] = encrypted_data

            if file_path.stem == ".env":
                with file_path.open('r') as file:
                    content = file.read()
                encrypted_data = self.encryption_of_data(data=content)
                all_encrypted_data[secret] = encrypted_data

        return all_encrypted_data
