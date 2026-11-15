
import pytest

# Import module validation.
# Nếu TV3 chưa tạo validation.py, pytest sẽ tạm bỏ qua file test này.
validation_module = pytest.importorskip("src.validation")

validate_input = validation_module.validate_input


# ==================================================
# TEST 1: DỮ LIỆU ĐẦU VÀO HỢP LỆ
# ==================================================

@pytest.mark.parametrize("speed, distance", [
    (0, 0),
    (0, 5),
    (30, 17.5),
    (60, 35),
    (80, 55),
    (100, 80),
    (120, 110),

    # Kiểm tra dữ liệu dạng chuỗi số
    ("60", "30"),
])
def test_valid_input(speed, distance):
    result = validate_input(speed, distance)

    assert result["valid"] is True
    assert result["speed"] == pytest.approx(float(speed))
    assert result["distance"] == pytest.approx(float(distance))
    assert result["error"] is None


# ==================================================
# TEST 2: DỮ LIỆU ĐẦU VÀO KHÔNG HỢP LỆ
# ==================================================

@pytest.mark.parametrize("speed, distance", [
    # Giá trị âm
    (-1, 10),
    (40, -0.1),

    # Sai định dạng
    ("abc", 10),
    (40, "abc"),

    # NaN và Infinity
    (float("nan"), 10),
    (40, float("nan")),
    (float("inf"), 10),
    (40, float("inf")),

    # Giá trị None
    (None, 10),
    (40, None),

    # Giá trị rỗng
    ("", 10),
    (40, ""),

    # Tốc độ vượt giới hạn 120 km/h
    (120.01, 110),
])
def test_invalid_input(speed, distance):
    result = validate_input(speed, distance)

    assert result["valid"] is False
    assert result["speed"] is None
    assert result["distance"] is None
    assert isinstance(result["error"], str)
    assert result["error"].strip() != ""
