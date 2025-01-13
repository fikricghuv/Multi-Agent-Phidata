from typing import Dict, Any, Optional
from phi.tools import Toolkit
from phi.utils.log import logger
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64


class RSAEncryptionTools(Toolkit):
    def __init__(self, private_key: Optional[bytes] = None, public_key: Optional[bytes] = None):
        """
        Inisialisasi RSAEncryptionTools dengan kunci private dan public.
        Jika tidak diberikan, kunci baru akan dibuat secara otomatis.
        """
        super().__init__(name="rsa_encryption_tools")

        if private_key and public_key:
            self.private_key = serialization.load_pem_private_key(private_key, password=None)
            self.public_key = serialization.load_pem_public_key(public_key)
        else:
            self.private_key, self.public_key = self._generate_keys()

        self.register(self.encrypt_message)
        self.register(self.decrypt_message)

    def _generate_keys(self) -> tuple:
        """
        Membuat pasangan kunci RSA (private dan public).
        Returns:
            tuple: (private_key, public_key) dalam format objek RSA.
        """
        logger.info("Generating new RSA key pair...")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        logger.info("Key pair generated successfully.")
        return private_key, public_key

    def get_serialized_keys(self) -> Dict[str, bytes]:
        """
        Mendapatkan kunci private dan public dalam format PEM.
        Returns:
            Dict[str, bytes]: Kunci private dan public dalam format PEM.
        """
        private_key_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return {"private_key": private_key_pem, "public_key": public_key_pem}

    def encrypt_message(self, message: str) -> str:
        """
        Mengenkripsi pesan menggunakan kunci public.
        Args:
            message (str): Pesan plaintext yang akan dienkripsi.
        Returns:
            str: Pesan terenkripsi dalam format base64.
        """
        logger.info("Encrypting message...")
        encrypted_message = self.public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        encrypted_base64 = base64.b64encode(encrypted_message).decode()
        logger.info("Message encrypted successfully.")
        return encrypted_base64

    def decrypt_message(self, encrypted_message: str) -> str:
        """
        Mendekripsi pesan menggunakan kunci private.
        Args:
            encrypted_message (str): Pesan terenkripsi dalam format base64.
        Returns:
            str: Pesan plaintext setelah didekripsi.
        """
        logger.info("Decrypting message...")
        encrypted_bytes = base64.b64decode(encrypted_message)
        decrypted_message = self.private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        plaintext_message = decrypted_message.decode()
        logger.info("Message decrypted successfully.")
        return plaintext_message
