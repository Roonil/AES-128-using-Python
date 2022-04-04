# AES-128-using-Python

Implementation of AES 128-Bit Encryption (and Decryption) using Python, without importing any libraries. It aims to better understand the process of the encryption, with computations of all steps in action. Supported modes are ECB, CBC, CFB, OFB and CTR.

# Usage

## Encryption
Set the Plaintext, Secret Key, IV (if applicable) and the mode of encryption in Creds.py, and then execute ```python3 Enc.py``` The encrypted Ciphertext gets displayed on the console.

## Decryption
Set the mode in Creds.py, and the encrypted Ciphertext in Dec.py and execute ```python3 Dec.py``` The decrypted cipher gets displayed on the console, along with raw output if applicable.
