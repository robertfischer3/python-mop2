import os
from cryptography.fernet import Fernet


class SimpleFileEncryption(object):

    def __init__(self, key_directory=None):
        if key_directory is None:
            self.key_directory = os.curdir
        elif os.path.isdir(key_directory):
            self.key_directory = key_directory
        else:
            raise IsADirectoryError

    def write_key(self,keyfile="privatekey.key"):
        """
        Generates a key and save it into a file. generate_key() function generates
         a fernet key, you need to keep this in a safe place, if you lose this key,
         you will be unable to decrypt data that was encrypted with this key.

        """
        key = Fernet.generate_key()

        with open(keyfile, "wb") as key_file:
            key_file.write(key)

    def load_key(self, keyfile="privatekey.key"):
        """
        Loads the key from the current directory named `key.key`
        """
        return open(keyfile, "rb").read()

    def encrypt(self, filename, key):
        """
        Given a filename (str) and key (bytes), it encrypts the file and write it
        """
        if not os.path.isfile(filename):
            raise FileExistsError

        f = Fernet(key)

        with open(filename, "rb") as plain_text_file:
            # read all file data
            file_data = plain_text_file.read()

        # encrypt data
        encrypted_data = f.encrypt(file_data)

        # write the encrypted file
        with open(filename, "wb") as file:
            file.write(encrypted_data)

    def decrypt(self, filename, key):
        """
        Given a filename (str) and key (bytes), it decrypts the file and write it
        """
        f = Fernet(key)
        with open(filename, "rb") as encrypted_file:
            # read the encrypted data
            encrypted_data = encrypted_file.read()
        # decrypt data
        decrypted_data = f.decrypt(encrypted_data)
        # write the original file
        with open(filename, "wb") as file:
            file.write(decrypted_data)

