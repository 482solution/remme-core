import hashlib

from sawtooth_signing import create_context


def generate_random_key():
    return create_context('secp256k1').new_random_private_key().as_hex()


# kecak256
def hash256(data):
    return hashlib.sha3_256(data).hexdigest()


def hash512(data):
    return hashlib.sha512(data).hexdigest()

