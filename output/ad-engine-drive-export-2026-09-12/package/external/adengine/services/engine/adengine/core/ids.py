import secrets, time

def new_id(prefix: str) -> str:
    return f"{prefix}_{int(time.time()*1000):x}{secrets.token_hex(4)}"
