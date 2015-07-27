from hashlib import sha512


def get_hash(text):
    return sha512(text.encode('utf-8')).hexdigest()


def check_hash(text, c_hash):
    return c_hash == get_hash(text)
