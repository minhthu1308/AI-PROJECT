import math

from src.rules import MAX_SPEED


def _to_float(value):
    """Chuyển value sang float hữu hạn. Ném ValueError nếu không hợp lệ."""
    if isinstance(value, bool) or value is None:
        raise ValueError("not a number")
    if isinstance(value, str):
        value = value.strip()
        if value == "":
            raise ValueError("empty")
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError("not a number")
    if math.isnan(number) or math.isinf(number):
        raise ValueError("nan or inf")
    return number


def _invalid(message):
    return {"valid": False, "speed": None, "distance": None, "error": message}


def validate_input(speed, distance):
    """Trả về dict: valid, speed, distance, error."""
    try:
        speed_value = _to_float(speed)
    except ValueError:
        return _invalid("invalid speed value.")
    if speed_value < 0 or speed_value > MAX_SPEED:
        return _invalid("invalid speed value.")

    try:
        distance_value = _to_float(distance)
    except ValueError:
        return _invalid("invalid distance value.")
    if distance_value < 0:
        return _invalid("invalid distance value.")

    return {
        "valid": True,
        "speed": speed_value,
        "distance": distance_value,
        "error": None,
    }
