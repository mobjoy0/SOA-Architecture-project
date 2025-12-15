import jwt

SECRET_KEY = "klrjklgerjhklbhjkesfjytdfsbhgdfbhjvdnjhdgfjhvbnwdgvbng"  # same secret your auth service uses

def verify_jwt(token, required_role=None):
    """
    Verify JWT token.
    Returns payload if valid, otherwise None.
    Optionally checks required_role.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

    if required_role and payload.get("role") != required_role:
        return None

    return payload