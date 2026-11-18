from src.rules import DELTA, MAX_SPEED, RULES


def calculate_d_min(speed):
    """Khoảng cách an toàn tối thiểu (m), kiểu float, không làm tròn.

    0 <= V <= 60 : D_min = 35 * V / 60   (V = 0 -> 0.0, V = 60 -> 35.0)
    60 < V <= 80 : 55
    80 < V <= 100: 70
    100 < V <= 120: 100
    """
    v = float(speed)
    if v < 0 or v > MAX_SPEED:
        raise ValueError("speed out of supported range 0-120 km/h")
    if v <= 60:
        return 35.0 * v / 60.0
    if v <= 80:
        return 55.0
    if v <= 100:
        return 70.0
    return 100.0


def _build_result(rule_id, d_min):
    rule = RULES[rule_id]
    return {
        "status": rule["status"],
        "message": rule["message"],
        "recommendation": rule["recommendation"],
        "rule_id": rule_id,
        "d_min": d_min,
    }


def evaluate_collision(speed, distance):
    """Luôn trả dict đủ 5 trường: status, message, recommendation, rule_id, d_min."""
    speed = float(speed)
    distance = float(distance)
    d_min = calculate_d_min(speed)

    if speed == 0 and distance == 0:
        return _build_result("R01", 0.0)
    if distance < d_min:
        return _build_result("R02", d_min)
    if distance <= d_min + DELTA:
        return _build_result("R03", d_min)
    return _build_result("R04", d_min)
