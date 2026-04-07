import string
import random
from datetime import datetime, timedelta


BASE62 = string.ascii_letters + string.digits


def generate_short_code(length: int = 6) -> str:
    return "".join(random.choices(BASE62, k=length))


def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]
    arr = []
    base = len(BASE62)
    while num:
        arr.append(BASE62[num % base])
        num //= base
    return "".join(reversed(arr))


def decode_base62(code: str) -> int:
    base = len(BASE62)
    num = 0
    for char in code:
        num = num * base + BASE62.index(char)
    return num


def generate_from_timestamp() -> str:
    timestamp = int(datetime.now().timestamp() * 1000)
    return encode_base62(timestamp)


def is_expired(expires_at: str) -> bool:
    if not expires_at:
        return False
    try:
        expire_date = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        return datetime.now() > expire_date
    except:
        return False


def format_expiry(days: int = 30) -> str:
    return (datetime.now() + timedelta(days=days)).isoformat()
