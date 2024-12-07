import base64
import os
from typing import Any

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from src.core.standards.logger import logger


class BaseEncryption:
    """基础加密类"""

    @classmethod
    def get_key(cls, key_id: str) -> bytes:
        """从密钥管理服务获取密钥"""
        # TODO: 实现密钥管理服务集成
        # 这里应该集成 AWS KMS 或其他密钥管理服务
        return base64.b64decode(os.getenv(f"ENCRYPTION_KEY_{key_id}", ""))


class AESEncryption(BaseEncryption):
    """AES加密实现"""

    @classmethod
    def encrypt(cls, data: Any, key_id: str) -> str:
        """AES加密"""
        try:
            # 获取密钥
            key = cls.get_key(key_id)

            # 生成随机IV
            iv = os.urandom(16)

            # 创建加密器
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()

            # 添加填充
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(str(data).encode()) + padder.finalize()

            # 加密
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

            # 组合IV和加密数据
            return base64.b64encode(iv + encrypted_data).decode()
        except Exception as e:
            logger.error(f"AES encryption failed: {e}")
            raise

    @classmethod
    def decrypt(cls, encrypted_data: str, key_id: str) -> Any:
        """AES解密"""
        try:
            # 获取密钥
            key = cls.get_key(key_id)

            # 解码数据
            raw_data = base64.b64decode(encrypted_data)
            iv = raw_data[:16]
            encrypted_data = raw_data[16:]

            # 创建解密器
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()

            # 解密
            padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

            # 移除填充
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()

            return data.decode()
        except Exception as e:
            logger.error(f"AES decryption failed: {e}")
            raise


class RSAEncryption(BaseEncryption):
    """RSA加密实现"""

    @classmethod
    def generate_key_pair(cls) -> tuple[bytes, bytes]:
        """生成RSA密钥对"""
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return private_pem, public_pem

    @classmethod
    def encrypt(cls, data: Any, key_id: str) -> str:
        """RSA加密"""
        try:
            # 获取公钥
            public_key = serialization.load_pem_public_key(
                cls.get_key(f"{key_id}_public")
            )

            # 加密
            encrypted_data = public_key.encrypt(
                str(data).encode(),
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )

            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"RSA encryption failed: {e}")
            raise

    @classmethod
    def decrypt(cls, encrypted_data: str, key_id: str) -> Any:
        """RSA解密"""
        try:
            # 获取私钥
            private_key = serialization.load_pem_private_key(
                cls.get_key(f"{key_id}_private"), password=None
            )

            # 解密
            decrypted_data = private_key.decrypt(
                base64.b64decode(encrypted_data),
                asym_padding.OAEP(
                    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )

            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"RSA decryption failed: {e}")
            raise


class FernetEncryption(BaseEncryption):
    """Fernet对称加密实现（简单且安全）"""

    @classmethod
    def generate_key(cls) -> bytes:
        """生成Fernet密钥"""
        return Fernet.generate_key()

    @classmethod
    def encrypt(cls, data: Any, key_id: str) -> str:
        """Fernet加密"""
        try:
            key = cls.get_key(key_id)
            f = Fernet(key)
            return f.encrypt(str(data).encode()).decode()
        except Exception as e:
            logger.error(f"Fernet encryption failed: {e}")
            raise

    @classmethod
    def decrypt(cls, encrypted_data: str, key_id: str) -> Any:
        """Fernet解密"""
        try:
            key = cls.get_key(key_id)
            f = Fernet(key)
            return f.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"Fernet decryption failed: {e}")
            raise
