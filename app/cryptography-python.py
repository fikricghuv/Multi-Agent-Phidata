from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Tuple

class RSATools:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self, key_size: int = 2048) -> Tuple[bytes, bytes]:
        """
        Generate RSA key pair.

        :param key_size: Size of the RSA keys (default: 2048).
        :return: Serialized private and public keys as bytes.
        """
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        self.public_key = self.private_key.public_key()

        # Serialize the keys
        private_key_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_key_bytes, public_key_bytes

    def encrypt(self, message: str, public_key_bytes: bytes) -> bytes:
        """
        Encrypt a message using the public key.

        :param message: The plaintext message to encrypt.
        :param public_key_bytes: The public key in PEM format.
        :return: Encrypted message as bytes.
        """
        public_key = serialization.load_pem_public_key(public_key_bytes)
        encrypted_message = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_message

    def decrypt(self, encrypted_message: bytes, private_key_bytes: bytes) -> str:
        """
        Decrypt an encrypted message using the private key.

        :param encrypted_message: The encrypted message as bytes.
        :param private_key_bytes: The private key in PEM format.
        :return: Decrypted plaintext message as a string.
        """
        private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
        decrypted_message = private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode()

from phi.tools import Toolkit

class RSAToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="rsa_agent")
        self.rsa_tools = RSATools()
        self.register(self.generate_keys)
        self.register(self.encrypt_message)
        self.register(self.decrypt_message)

    def generate_keys(self) -> Tuple[str, str]:
        """
        Generate RSA key pair and return them as strings.
        """
        private_key, public_key = self.rsa_tools.generate_keys()
        return private_key.decode(), public_key.decode()

    def encrypt_message(self, message: str, public_key: str) -> bytes:
        """
        Encrypt a message using the provided public key.
        """
        return self.rsa_tools.encrypt(message, public_key.encode())

    def decrypt_message(self, encrypted_message: bytes, private_key: str) -> str:
        """
        Decrypt an encrypted message using the provided private key.
        """
        return self.rsa_tools.decrypt(encrypted_message, private_key.encode())
    
# Inisialisasi agen
rsa_agent = RSAToolkit()

# Generate key pair
private_key, public_key = rsa_agent.generate_keys()
print("Private Key:", private_key)
print("Public Key:", public_key)

# Encrypt a message
message = "Hello, this is a test message."
encrypted_message = rsa_agent.encrypt_message(message, public_key)
print("Encrypted Message:", encrypted_message)

# Decrypt the message
decrypted_message = rsa_agent.decrypt_message(encrypted_message, private_key)
print("Decrypted Message:", decrypted_message)
