import bcrypt


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.

    Raises:
        ValueError: If the password is not a non-empty string.
        Exception: If there is an error hashing the password.
    """
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string")

    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
        return hashed_password
    except Exception as e:
        raise Exception(f"Error hashing password: {e}")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password.

    Args:
        password (str): The password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.

    Raises:
        ValueError: If the password or hashed password is not a non-empty string.
        Exception: If there is an error verifying the password.
    """
    if not isinstance(password, str) or not password:
        raise ValueError("Password must be a non-empty string")

    if not isinstance(hashed_password, str) or not hashed_password:
        raise ValueError("Hashed password must be a non-empty string")

    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception as e:
        raise Exception(f"Error verifying password: {e}")
