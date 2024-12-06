import secrets
import string

alphanum_lower = string.ascii_lowercase + string.digits

def rand_str(num = 4):
    """Generate random lowercase alphanumeric string of length num.

    :meta private:
    """
    return "".join(secrets.choice(alphanum_lower) for _ in range(num))