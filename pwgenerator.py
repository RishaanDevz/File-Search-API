import hashlib

# Generate the hash for your chosen password
password = "insert-pw-here"
password_hash = hashlib.sha256(password.encode()).hexdigest()
print(password_hash)
