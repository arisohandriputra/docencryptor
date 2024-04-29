import os
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidTag
from colorama import Fore, Back, Style, init

init()

ENCRYPTION_FLAG = b"899129"
NONCE_SIZE = 12
TAG_SIZE = 16
KEY_SIZE = 32

def generate_key(key_file):
    key = os.urandom(KEY_SIZE) 
    with open(key_file, "wb") as kf:
        kf.write(key)
    print(Fore.GREEN + f"AES-256 key successfully generated: '{key_file}'")

def encrypt_files(file_list, key_file):
    with open(key_file, "rb") as kf:
        key = kf.read()

    if len(key) != KEY_SIZE:
        print(Fore.RED + "Invalid key length.The key must be 32 bytes.")
        return

    all_successful = True

    for input_file in file_list:
        with open(input_file, "rb") as f:
            data = f.read()

        if data.startswith(ENCRYPTION_FLAG):
            print(Fore.RED + f"File '{input_file}' already encrypted.")
            all_successful = False
            continue

        nonce = os.urandom(NONCE_SIZE)
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()

        encrypted_data = encryptor.update(data) + encryptor.finalize()

        with open(input_file, "wb") as f:
            f.write(ENCRYPTION_FLAG + nonce + encryptor.tag + encrypted_data)

        print(Fore.GREEN + f"File '{input_file}' successfully encrypted.")

    if all_successful:
        print(Fore.GREEN + "All the files were encrypted successfully.")
    else:
        print(Fore.YELLOW + "Not all files are successfully encrypted.")

def decrypt_files(file_list, key_file):
    with open(key_file, "rb") as kf:
        key = kf.read() 

    if len(key) != KEY_SIZE:
        print(Fore.RED + "Invalid key length. The key must be 32 bytes.")
        return

    all_successful = True

    for input_file in file_list:
        with open(input_file, "rb") as f:
            encrypted_data = f.read()

        if not encrypted_data.startswith(ENCRYPTION_FLAG):
            print(Fore.RED + f"File '{input_file}' doesn't look encrypted.")
            all_successful = False
            continue

        if len(encrypted_data) < len(ENCRYPTION_FLAG) + NONCE_SIZE + TAG_SIZE:
            print(Fore.RED + f"File '{input_file}' is too short for a valid encrypted file.")
            all_successful = False
            continue

        nonce = encrypted_data[len(ENCRYPTION_FLAG):len(ENCRYPTION_FLAG) + NONCE_SIZE]
        tag = encrypted_data[len(ENCRYPTION_FLAG) + NONCE_SIZE:len(ENCRYPTION_FLAG) + NONCE_SIZE + TAG_SIZE]
        data = encrypted_data[len(ENCRYPTION_FLAG) + NONCE_SIZE + TAG_SIZE:]

        try:
            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
            decryptor = cipher.decryptor()

            decrypted_data = decryptor.update(data) + decryptor.finalize()

            with open(input_file, "wb") as f:
                f.write(decrypted_data)

            print(Fore.GREEN + f"File '{input_file}' successfully decrypted.")

        except InvalidTag:
            print(Fore.RED + f"Decryption failed for '{input_file}'. Possible incorrect keys, corrupted data, or altered tags.")
            all_successful = False

    if all_successful:
        print(Fore.GREEN + "All files are successfully decrypted.")
    else:
        print(Fore.YELLOW + "Not all files are successfully decrypted.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(Style.BRIGHT + Fore.RED + "This program only runs on Windows 10 and later.")
        print(Fore.WHITE + Back.BLACK + "Encryption Technology Used:")
        print("• Algorithm: AES-256.")
        print("• Mode of Operation: GCM (Galois/Counter Mode)")
        print("• Key Size: 256 bits (32 bytes)")
        print("• Nonce/IV (Initialization Vector): 12 bytes")
        print("• Tag: 16 bytes (Used for authentication in GCM)")
        print("• Encryption Library: Cryptography with hazmat backend (Hardware-assisted Cryptography)")
        print(Fore.WHITE + Back.YELLOW + "For use as a third-party tool, contact the developer's email:")
        print(Fore.BLUE + Back.BLACK + "arisohandriputra@gmail.com.")
        print(Fore.WHITE + "********************")
        print("© 2017 - 2024 Ari Sohandri Putra")
        sys.exit(1)

    command = sys.argv[1]

    if command == "generate_key":
        if len(sys.argv) < 3:
            print("Usage: <file_name> generate_key <file_key>")
            sys.exit(1)
        key_file = sys.argv[2]
        generate_key(key_file)
    elif command == "encrypt":
        if len(sys.argv) < 4:
            print("Usage: <file_name> encrypt <file_key> <file1> <file2> ...")
            sys.exit(1)
        key_file = sys.argv[2]
        file_list = sys.argv[3:]
        encrypt_files(file_list, key_file)
    elif command == "decrypt":
        if len(sys.argv) < 4:
            print("Usage: <file_name> decrypt <file_key> <file1> <file2> ...")
            sys.exit(1)
        key_file = sys.argv[2]
        file_list = sys.argv[3:]
        decrypt_files(file_list, key_file)
    else:
        print(Fore.RED + "Command not recognized. Use 'generate_key', 'encrypt', or 'decrypt'.")
        sys.exit(1)