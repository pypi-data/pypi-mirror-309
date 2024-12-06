### About
Bytecript is a python package for easy data encryption / decryption with password.

### Usage
```py

# main.py

from bytecrypt.bytecrypt import encrypt_bytes
from bytecrypt.bytecrypt import decrypt_bytes

encrypted_data = encrypt_bytes(b"secret", b"password")
decrypted_data = decrypt_bytes(encrypted_data, b"password")

print("\nEncrypted data: " + str(encrypted_data.decode("utf-8")))
print("\nDecrypted data: " + str(decrypted_data.decode("utf-8")))


```