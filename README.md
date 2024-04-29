# DocEncryptor
This code uses the AES (Advanced Encryption Standard) encryption algorithm with a key size of 256 bits and a GCM (Galois/Counter Mode) mode of operation.
> Encryption Technology Used:
* Algorithm: AES-256
* Mode of Operation: GCM (Galois/Counter Mode)
* Key Size: 256 bits (32 bytes)
* Nonce/IV (Initialization Vector): 12 bytes
* Tag: 16 bytes (Used for authentication in GCM)
* Encryption Library: Cryptography with hazmat backend (Hardware-assisted Cryptography)
# Is it Safe and Strong?
The AES algorithm with a key size of 256 bits is the industry standard for symmetric encryption and is considered secure and strong if applied correctly. GCM is a mode of operation that offers encryption along with authentication, so it can detect changes or manipulation of data during transmission or storage.
# This code uses several third-party libraries. The following are the third-party libraries:
> Cryptography: pip install Cryptography
* Used for various cryptographic operations, such as encryption and decryption.
* Allows the use of encryption algorithms such as AES with various modes of operation.
* In this code, the hazmat backend is used to execute Cipher functions, algorithms, and modes.
> Colorama: pip install Colorama
* Used to give color and style to text on a terminal or console.
* Helps make text output more attractive and readable with the use of different colors.
* In this code, it is used to print text with green, red, yellow colors, and specific styles (for example, Fore, Back, and Style).
# Conclusion
In general, this code uses strong and secure encryption technology, but it is still important to follow best security practices in key management and encryption operations. Be sure to understand the importance of keeping keys confidential, and ensure nonce is not used repeatedly to maintain security and encryption strength.
