from ecies.utils import generate_key
from ecies import encrypt, decrypt

# ----------------------------------
# 1. Generate ECC key pair (secp256k1)
# ----------------------------------
secp_k = generate_key()
privhex = secp_k.to_hex()                     # Private key (hex)
pubhex = secp_k.public_key.format(True).hex() # Public key (compressed hex)

print("Private Key:", privhex)
print("Public Key :", pubhex)

# ----------------------------------
# 2. Plain text message
# ----------------------------------
message = "Hello boss! ECIES encryption working 💪"
message_bytes = message.encode("utf-8")

# ----------------------------------
# 3. Encryption (using PUBLIC key)
# ----------------------------------
ciphertext = encrypt(pubhex, message_bytes)
print("Encrypted (hex):", ciphertext.hex())

# ----------------------------------
# 4. Decryption (using PRIVATE key)
# ----------------------------------
decrypted_bytes = decrypt(privhex, ciphertext)
decrypted_message = decrypted_bytes.decode("utf-8")

print("Decrypted Message:", decrypted_message)