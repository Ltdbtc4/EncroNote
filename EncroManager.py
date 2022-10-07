import os

from cryptography.fernet import Fernet

import pickle


def is_encrypted(file_path):
    DF, EF = ReceiveData()
    for file in EF:
        if file == file_path:
            return True
    return False


def ReceiveData():
    with open("Dfiles", "rb") as file:
        DF = pickle.load(file)
    with open("Efiles", "rb") as file:
        EF = pickle.load(file)
    print(EF, DF)
    return DF, EF


def return_key():
    with open("Key", "rb") as file:
        Key = file.read()
    return Key


def return_file_contents_decrypted(file_name):
    with open(f"{file_name}", "rb") as file:
        contents = file.read()
    return Manager.decrypt(contents)


def return_file_contents_encrypted(file_name):
    with open(f"{file_name}", "rb") as file:
        contents = file.read()
    return contents


def encrypt_file(file_name):
    store_data(file_name, "Encrypt")
    with open(f"{file_name}", "rb") as file:
        contents = file.read()
    Encrypted_contents = Manager.encrypt(contents)
    with open(f"{file_name}", "wb") as file:
        file.write(Encrypted_contents)


def decrypt_file(file_name):
    store_data(file_name, "Decrypt")
    with open(f"{file_name}", "rb") as file:
        contents = file.read()
    Decrypted_contents = Manager.decrypt(contents)
    with open(f"{file_name}", "wb") as file:
        file.write(Decrypted_contents)


def return_eligible_files(directory):
    eligible_files = []
    files = os.listdir(directory)
    for file in files:
        ext = os.path.splitext(file)
        if ext[1] == ".txt":
            eligible_files.append(file)
    return eligible_files


def store_data(FilePath, Instruction):
    DF, EF = ReceiveData()
    if is_encrypted(FilePath) and Instruction == "Encrypt":
        return 0
    if is_encrypted(FilePath) and Instruction == "Decrypt":
        EF.remove(FilePath)
        DF.append(FilePath)
    if not is_encrypted(FilePath) and Instruction == "Encrypt":
        try:
            DF.remove(FilePath)
        except ValueError:
            pass
        EF.append(FilePath)
    if not is_encrypted(FilePath) and Instruction == "Decrypt":
        return 0

    with open("Dfiles", "wb") as file:
        pickle.dump(DF, file)
    with open("Efiles", "wb") as file:
        pickle.dump(EF, file)


def PurgeData():
    PURGE = ["STARTED"]
    with open("Dfiles", "wb") as file:
        pickle.dump(PURGE, file)
    with open("Efiles", "wb") as file:
        pickle.dump(PURGE, file)


key = return_key()

Manager = Fernet(key)
