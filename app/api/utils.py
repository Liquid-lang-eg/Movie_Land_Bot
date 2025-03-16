import hashlib

def hash_id(user_id: int) -> str:
    return hashlib.sha256(str(user_id).encode()).hexdigest()
