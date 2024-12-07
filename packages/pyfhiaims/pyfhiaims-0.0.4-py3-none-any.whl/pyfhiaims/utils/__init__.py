"""Various utilities for pyaims"""


def is_number_string(s: str) -> bool:
    """Checks if s is a string made of float numbers and optionally comment sign.

    Parameters:
        s: str
            A string to check

    """
    allowed_chars = set("-.# ")
    return all(char.isdigit() or char in allowed_chars for char in s)