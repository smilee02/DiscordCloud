import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

def write_key():
    """
    Generates a key and save it to .env
    """
    key = Fernet.generate_key()
    set_key(key_to_set="SECRET_KEY", value_to_set=key)
        
def load_key():
    """
    Loads the key from the current .env
    """
    load_dotenv()

    KEY = (os.getenv("SECRET_KEY"))
    return KEY

def get_encryptor():
    fernet = Fernet(load_key())
    return fernet