from cryptography.fernet import Fernet

class FernetCrypto:
    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt_data(secret_key, data):
        fernet = Fernet(secret_key)
        encrypted_data = fernet.encrypt(data.encode())
        return encrypted_data

    @staticmethod
    def decrypt_data(secret_key, encrypted_data):
        fernet = Fernet(secret_key)
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return decrypted_data