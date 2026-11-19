import pytest
from unittest.mock import patch

# Bỏ qua toàn bộ file test nếu module src.main hoặc các thành phần phụ thuộc chưa sẵn sàng.
main_module = pytest.importorskip("src.main")
handle_evaluate = main_module.handle_evaluate

REQUIRED_FIELDS = {"status", "message", "recommendation", "rule_id", "d_min"}

VALID_VALIDATION = {"valid": True, "speed": 60.0, "distance": 35.0, "error": None}
VALID_INFERENCE = {
    "status": "WARNING",
    "message": "Có nguy cơ va chạm.",
    "recommendation": "Hãy thận trọng và chủ động xử lý.",
    "rule_id": "R03",
    "d_min": 35.0,
}


def assert_error_result(result):
    """Kết quả ERROR phải có đủ trường và nội dung không rỗng."""
    assert REQUIRED_FIELDS.issubset(result.keys())
    assert result["status"] == "ERROR"
    assert isinstance(result["message"], str) and result["message"].strip() != ""
    assert isinstance(result["recommendation"], str) and result["recommendation"].strip() != ""
    assert result["rule_id"] is None
    assert result["d_min"] is None


# ==================================================
# TEST 1: LUỒNG ĐIỀU PHỐI BẰNG MOCK
# ==================================================

def test_invalid_input_stops_before_inference():
    """Dữ liệu không hợp lệ -> ERROR và KHÔNG gọi evaluate_collision."""
    fake_validation = {
        "valid": False,
        "speed": None,
        "distance": None,
        "error": "Invalid speed value.",
    }

    with patch.object(main_module, "validate_input", return_value=fake_validation) as mock_val, \
         patch.object(main_module, "evaluate_collision") as mock_inf:

        result = handle_evaluate("-10", "20")

        mock_val.assert_called_once_with("-10", "20")
        mock_inf.assert_not_called()

        assert_error_result(result)
        assert result["message"] == "Invalid speed value."


def test_invalid_input_without_error_text_uses_default_message():
    """Validation không kèm nội dung lỗi -> dùng thông báo mặc định."""
    fake_validation = {"valid": False, "speed": None, "distance": None, "error": None}

    with patch.object(main_module, "validate_input", return_value=fake_validation), \
         patch.object(main_module, "evaluate_collision") as mock_inf:

        result = handle_evaluate("x", "y")

        mock_inf.assert_not_called()
        assert_error_result(result)


def test_valid_input_passes_clean_floats_to_inference():
    """Dữ liệu hợp lệ -> truyền float đã chuẩn hóa (không phải str) sang evaluate_collision."""
    with patch.object(main_module, "validate_input", return_value=VALID_VALIDATION) as mock_val, \
         patch.object(main_module, "evaluate_collision", return_value=VALID_INFERENCE) as mock_inf:

        result = handle_evaluate("60", "35")

        mock_val.assert_called_once_with("60", "35")
        mock_inf.assert_called_once_with(60.0, 35.0)

        # Kết quả được giữ nguyên, không đổi tên hay bỏ trường
        assert result == VALID_INFERENCE


def test_inference_result_is_forwarded_unchanged():
    """Với mọi trạng thái hợp lệ, main không được sửa kết quả của Inference."""
    for status, rule in [("SAFE", "R04"), ("WARNING", "R03"), ("DANGER", "R02")]:
        fake_inference = {**VALID_INFERENCE, "status": status, "rule_id": rule}
        with patch.object(main_module, "validate_input", return_value=VALID_VALIDATION), \
             patch.object(main_module, "evaluate_collision", return_value=fake_inference):
            assert handle_evaluate("60", "35") == fake_inference


# ----- Các tình huống lỗi bất thường -----

def test_validation_raises_exception():
    """Validation ném ngoại lệ -> ERROR, không sập, không gọi Inference."""
    with patch.object(main_module, "validate_input", side_effect=RuntimeError("Lỗi bất ngờ")), \
         patch.object(main_module, "evaluate_collision") as mock_inf:

        result = handle_evaluate("50", "20")

        mock_inf.assert_not_called()
        assert_error_result(result)
        assert "Lỗi bất ngờ" in result["message"]


def test_inference_raises_exception():
    """Inference ném ngoại lệ -> ERROR, không sập."""
    with patch.object(main_module, "validate_input", return_value=VALID_VALIDATION), \
         patch.object(main_module, "evaluate_collision", side_effect=ValueError("boom")):

        result = handle_evaluate("60", "35")

        assert_error_result(result)
        assert "boom" in result["message"]


@pytest.mark.parametrize("bad_inference", [
    {"status": "SAFE"},                                          # thiếu nhiều trường
    {k: v for k, v in VALID_INFERENCE.items() if k != "d_min"},    # thiếu d_min
    {k: v for k, v in VALID_INFERENCE.items() if k != "rule_id"},  # thiếu rule_id
    {**VALID_INFERENCE, "status": "UNKNOWN"},                      # status ngoài SAFE/WARNING/DANGER
    None,                                                          # không phải dict
    "WARNING",                                                     # không phải dict
])
def test_malformed_inference_result_returns_error(bad_inference):
    """Inference trả kết quả sai cấu trúc -> ERROR."""
    with patch.object(main_module, "validate_input", return_value=VALID_VALIDATION), \
         patch.object(main_module, "evaluate_collision", return_value=bad_inference):

        result = handle_evaluate("60", "35")

        assert_error_result(result)


@pytest.mark.parametrize("bad_validation", [None, "invalid", [], {}])
def test_malformed_validation_result_returns_error_without_inference(bad_validation):
    """Validation trả kết quả sai cấu trúc -> ERROR, không gọi Inference."""
    with patch.object(main_module, "validate_input", return_value=bad_validation), \
         patch.object(main_module, "evaluate_collision") as mock_inf:

        result = handle_evaluate("60", "35")

        mock_inf.assert_not_called()
        assert_error_result(result)


# ==================================================
# TEST 2: KIỂM THỬ TÍCH HỢP (DỮ LIỆU ĐẦU VÀO DẠNG CHUỖI NHƯ TỪ UI)
# ==================================================

VALID_CASES = [
    # raw_speed, raw_distance, expected_status, expected_rule, expected_d_min
    ("0", "0", "DANGER", "R01", 0.0),                      # TC01
    ("0", "5", "WARNING", "R03", 0.0),                     # TC02
    ("0", "10", "WARNING", "R03", 0.0),                    # TC03
    ("0", "10.01", "SAFE", "R04", 0.0),                    # TC04
    ("30", "17.49", "DANGER", "R02", 17.5),                # TC05
    ("30", "17.5", "WARNING", "R03", 17.5),                # TC06
    ("30", "27.5", "WARNING", "R03", 17.5),                # TC07
    ("30", "27.51", "SAFE", "R04", 17.5),                  # TC08
    ("59.99", "34.99", "DANGER", "R02", 35 * 59.99 / 60),  # TC09
    ("60", "34.99", "DANGER", "R02", 35.0),                # TC10
    ("60", "35", "WARNING", "R03", 35.0),                  # TC11
    ("60", "45", "WARNING", "R03", 35.0),                  # TC12
    ("60", "45.01", "SAFE", "R04", 35.0),                  # TC13
    ("80", "55", "WARNING", "R03", 55.0),                  # TC14
    ("80.01", "69.99", "DANGER", "R02", 70.0),             # TC15
    ("100", "80", "WARNING", "R03", 70.0),                 # TC16
    ("100.01", "99.99", "DANGER", "R02", 100.0),           # TC17
    ("120", "110", "WARNING", "R03", 100.0),               # TC18
]

INVALID_CASES = [
    ("120.01", "110"),   # TC19 tốc độ vượt giới hạn
    ("-1", "10"),        # TC20 tốc độ âm
    ("40", "-0.1"),      # TC21 khoảng cách âm
    ("abc", "10"),       # TC22 tốc độ không phải số
    ("40", "nan"),       # TC23 khoảng cách NaN
    ("40", "inf"),       # TC24 khoảng cách Infinity
    ("", "10"),          # TC25 thiếu tốc độ
    ("40", ""),          # TC26 thiếu khoảng cách
    # Các trường hợp biên và dữ liệu rỗng bổ sung
    ("nan", "10"),
    ("inf", "10"),
    ("40", "abc"),
    ("   ", "10"),
    ("40", "   "),
    ("", ""),
]


@pytest.mark.parametrize(
    "raw_speed, raw_distance, expected_status, expected_rule, expected_d_min",
    VALID_CASES,
)
def test_integration_valid_cases(
    raw_speed, raw_distance, expected_status, expected_rule, expected_d_min
):
    """Toàn trình UI -> main -> validation -> inference với dữ liệu hợp lệ."""
    result = handle_evaluate(raw_speed, raw_distance)

    assert REQUIRED_FIELDS.issubset(result.keys())
    assert result["status"] == expected_status
    assert result["rule_id"] == expected_rule
    assert result["d_min"] == pytest.approx(expected_d_min)
    assert isinstance(result["message"], str) and result["message"].strip() != ""
    assert isinstance(result["recommendation"], str) and result["recommendation"].strip() != ""


@pytest.mark.parametrize("raw_speed, raw_distance", INVALID_CASES)
def test_integration_invalid_cases(raw_speed, raw_distance):
    """Toàn trình với dữ liệu không hợp lệ: phải ra ERROR, không có rule_id và d_min."""
    result = handle_evaluate(raw_speed, raw_distance)

    assert_error_result(result)


def test_integration_accepts_numeric_types_too():
    """Giao diện thường gửi str, nhưng số thật (int/float) vẫn phải xử lý được."""
    result = handle_evaluate(60, 35.0)

    assert result["status"] == "WARNING"
    assert result["rule_id"] == "R03"
