from cryptography.fernet import Fernet

# Generate a new encryption key
key = Fernet.generate_key()

# Print the key (store this securely)
print(key.decode())