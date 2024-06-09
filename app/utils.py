import hashlib
import random
import string


def generate_salt(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation + string.ascii_uppercase
    return ''.join(random.choice(characters) for _ in range(length))


def compute_sha256(input_string, salt=None):
    if not salt:
        salt = generate_salt()  # Generate a random salt if none is provided
    salted_input = salt + input_string

    # Create a new sha256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the bytes-like object (salted string converted to bytes)
    sha256_hash.update(salted_input.encode('utf-8'))

    # Get the hexadecimal representation of the digest
    return salt, sha256_hash.hexdigest()


def verify_password(input_string, stored_salt, stored_hash):
    _, new_hash = compute_sha256(input_string, stored_salt)
    return new_hash == stored_hash
