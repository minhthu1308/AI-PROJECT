
import pytest

# Import module inference.
# Nếu TV3 chưa tạo inference.py, pytest sẽ tạm bỏ qua file test này.
inference_module = pytest.importorskip("src.inference")

calculate_d_min = inference_module.calculate_d_min
evaluate_collision = inference_module.evaluate_collision


# ==================================================
# TEST 1: KIỂM TRA HÀM calculate_d_min()
# ==================================================

@pytest.mark.parametrize("speed, expected_d_min", [
    (0, 0.0),
    (30, 17.5),
    (59.99, 35 * 59.99 / 60),
    (60, 35.0),
    (80, 55.0),
    (80.01, 70.0),
    (100, 70.0),
    (100.01, 100.0),
    (120, 100.0),
])
def test_calculate_d_min(speed, expected_d_min):
    result = calculate_d_min(speed)

    # Kết quả phải là số thực (float)
    assert isinstance(result, float)

    # So sánh kết quả với khoảng cách mong đợi
    assert result == pytest.approx(expected_d_min)


# ==================================================
# TEST 2: KIỂM TRA HÀM evaluate_collision()
# ==================================================

@pytest.mark.parametrize(
    "speed, distance, expected_status, expected_rule, expected_d_min",
    [
        # TC01 - TC04: Speed = 0
        (0, 0, "DANGER", "R01", 0.0),
        (0, 5, "WARNING", "R03", 0.0),
        (0, 10, "WARNING", "R03", 0.0),
        (0, 10.01, "SAFE", "R04", 0.0),

        # TC05 - TC08: Speed = 30
        (30, 17.49, "DANGER", "R02", 17.5),
        (30, 17.5, "WARNING", "R03", 17.5),
        (30, 27.5, "WARNING", "R03", 17.5),
        (30, 27.51, "SAFE", "R04", 17.5),

        # TC09 - TC10: Speed gần và bằng 60
        (59.99, 34.99, "DANGER", "R02", 35 * 59.99 / 60),
        (60, 34.99, "DANGER", "R02", 35.0),

        # TC11 - TC13: Speed = 60
        (60, 35, "WARNING", "R03", 35.0),
        (60, 45, "WARNING", "R03", 35.0),
        (60, 45.01, "SAFE", "R04", 35.0),

        # TC14 - TC15: Speed = 80 và vừa vượt 80
        (80, 55, "WARNING", "R03", 55.0),
        (80.01, 69.99, "DANGER", "R02", 70.0),

        # TC16 - TC17: Speed = 100 và vừa vượt 100
        (100, 80, "WARNING", "R03", 70.0),
        (100.01, 99.99, "DANGER", "R02", 100.0),

        # TC18: Speed = 120
        (120, 110, "WARNING", "R03", 100.0),
    ],
)
def test_evaluate_collision(
    speed,
    distance,
    expected_status,
    expected_rule,
    expected_d_min
):
    result = evaluate_collision(speed, distance)

    # Kiểm tra kết quả có đầy đủ 5 trường bắt buộc
    required_fields = {
        "status",
        "message",
        "recommendation",
        "rule_id",
        "d_min",
    }

    assert isinstance(result, dict)
    assert required_fields.issubset(result.keys())

    # Kiểm tra trạng thái và luật được áp dụng
    assert result["status"] == expected_status
    assert result["rule_id"] == expected_rule

    # Kiểm tra khoảng cách an toàn tối thiểu
    assert isinstance(result["d_min"], float)
    assert result["d_min"] == pytest.approx(expected_d_min)

    # Kiểm tra nội dung thông báo
    assert isinstance(result["message"], str)
    assert result["message"].strip() != ""

    # Kiểm tra khuyến nghị
    assert isinstance(result["recommendation"], str)
    assert result["recommendation"].strip() != ""
