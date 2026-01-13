BASE62_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
BASE = 62


def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62_ALPHABET[0]

    chars = []
    while num > 0:
        num, rem = divmod(num, BASE)
        chars.append(BASE62_ALPHABET[rem])

    return "".join(reversed(chars))


def decode_base62(code: str) -> int:
    num = 0
    for char in code:
        num = num * BASE + BASE62_ALPHABET.index(char)
    return num
