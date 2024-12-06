from hashlib import sha256


def hash(input: bytearray) -> bytearray:
    """
    Returns the SHA-256 digest in a byte array
    """
    h = sha256()
    h.update(input)
    return h.digest()


def string2bytearray(string: str, encoding="utf-8") -> bytearray:
    """
    Transforms the passed string to a byte array (with default encoding as `utf-8`)
    """
    return bytearray(str.encode(string, encoding))
