def hide(secret: str) -> str:
    if len(secret) < 3:
        return "*" * len(secret)
    return secret[0] + ("*" * (len(secret) - 2)) + secret[-1]
