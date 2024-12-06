import yaml
from cryptography.fernet import Fernet
from hashlib import pbkdf2_hmac
import base64
import os
from .accept_terms import get_installation_path

def decrypt_credentials():
    base_path = get_installation_path()
    agreement_file_path = os.path.join(base_path, 'setup', 'agreement.txt')
    credentials_file_path = os.path.join(base_path, 'configs', 'credentials.yaml')

    with open(credentials_file_path, 'r') as file:
        encrypted_credentials = yaml.safe_load(file)
    
    encrypted_username = encrypted_credentials['username'].encode()
    encrypted_password = encrypted_credentials['password'].encode()

    with open(agreement_file_path, 'r') as file:
        line = file.readline()

    salt = 'agreement.txt'.encode()
    key = pbkdf2_hmac('sha256', line.encode(), salt, 100000)
    cipher_suite = Fernet(base64.urlsafe_b64encode(key))

    # Decrypt the credentials
    try:
        username = cipher_suite.decrypt(encrypted_username).decode()
        password = cipher_suite.decrypt(encrypted_password).decode()
        return username, password
        # Use the decrypted credentials
        # For example, to connect to a website
        # connect_to_website(username, password)
    except Exception as e:
        print("Decryption failed:", e)
