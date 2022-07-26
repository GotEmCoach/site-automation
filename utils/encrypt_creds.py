import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

import secrets
import base64
import getpass
from pathlib import Path
import os

UPPATH = Path(os.path.abspath(__file__)).parents[1]


# Code is derived from https://www.thepythoncode.com/article/encrypt-decrypt-files-symmetric-python

def generate_salt(size=16):
    """Generate the salt used for key derivation, 
    `size` is the length of the salt to generate"""
    return secrets.token_bytes(size)


def derive_key(salt, password):
    """Derive the key from the `password` using the passed `salt`"""
    derived_backend = default_backend()
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=derived_backend)
    return kdf.derive(password.encode())


def load_salt():
    # load salt from salt.salt file
    return open(f"{UPPATH}/credentials/salt.salt", "rb").read()


def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    """
    Generates a key from a `password` and the salt.
    If `load_existing_salt` is True, it'll load the salt from a file
    in the current directory called "salt.salt".
    If `save_salt` is True, then it will generate a new salt
    and save it to "salt.salt"
    """
    if load_existing_salt:
        # load existing salt
        salt = load_salt()
    elif save_salt:
        # generate new salt and save it
        salt = generate_salt(salt_size)
        with open(f"{UPPATH}/credentials/salt.salt", "wb") as salt_file:
            salt_file.write(salt)
    # generate the key from the salt and the password
    derived_key = derive_key(salt, password)
    # encode it using Base 64 and return it
    return base64.urlsafe_b64encode(derived_key)


def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(f"{filename}.enc", "wb") as file:
        file.write(encrypted_data)


def main():
    password = getpass.getpass("Enter the password for encryption: ")
    new_key = generate_key(password)
    credential_path = Path(f"{UPPATH}/credentials/credentials.json")
    encrypt(credential_path, key=new_key)
    os.remove(credential_path)

if __name__ == "__main__":
    main()