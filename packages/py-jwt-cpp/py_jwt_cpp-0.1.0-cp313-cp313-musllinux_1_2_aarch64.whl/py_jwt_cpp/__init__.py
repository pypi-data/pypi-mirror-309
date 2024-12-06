from typing import Dict
from .jwt_cpp import cpp_encode

class InvalidClaimError(Exception):
    pass

def encode(data: Dict[str, str], private_key: str):
    invalid_keys = [k for k, v in data.items() if not isinstance(v, str)]
    if invalid_keys:
        raise InvalidClaimError(
            f"all values in data should be string. Invalid keys: {invalid_keys}"
        )

    return cpp_encode(data, private_key)
