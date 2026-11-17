"""
main.py - Module điều phối chính của hệ thống (TV5)

Trách nhiệm (theo module_contracts.md):
    - Nhận dữ liệu từ giao diện (interface.py - TV4) qua handle_evaluate(speed, distance).
    - Gọi validate_input() (TV3) trước; nếu không hợp lệ thì trả ERROR, KHÔNG gọi evaluate_collision().
    - Nếu hợp lệ, dùng speed/distance đã chuẩn hóa để gọi evaluate_collision() (TV3).
    - Chuyển kết quả về giao diện, giữ nguyên tên các trường.

KHÔNG làm trong module này:
    - Không tự viết lại validation, công thức D_min hay luật IF-THEN.

Cách chạy (từ thư mục gốc của dự án):
    python -m src.main
"""

from src.validation import validate_input
from src.inference import evaluate_collision


# Năm trường bắt buộc của kết quả evaluate_collision() (module_contracts.md, mục 1.2).
REQUIRED_FIELDS = frozenset({"status", "message", "recommendation", "rule_id", "d_min"})

# Ba trạng thái hợp lệ do Inference Engine trả về (ERROR do TV5 tạo, không do Inference).
INFERENCE_STATUSES = frozenset({"SAFE", "WARNING", "DANGER"})

DEFAULT_VALIDATION_MESSAGE = "Dữ liệu đầu vào không hợp lệ."
DEFAULT_ERROR_RECOMMENDATION = (
    "Vui lòng kiểm tra và nhập lại tốc độ (0 - 120 km/h) "
    "và khoảng cách (>= 0 m) hợp lệ."
)
SYSTEM_ERROR_RECOMMENDATION = "Vui lòng thử lại hoặc liên hệ nhóm phát triển."


def _error_result(message, recommendation) -> dict:
    """Tạo kết quả ERROR (không có luật R01-R04 và d_min vì chưa/không có suy luận)."""
    return {
        "status": "ERROR",
        "message": message,
        "recommendation": recommendation,
        "rule_id": None,
        "d_min": None,
    }


def _is_valid_inference_result(result) -> bool:
    """Chỉ KIỂM TRA cấu trúc kết quả của Inference, không sửa nội dung."""
    return (
        isinstance(result, dict)
        and REQUIRED_FIELDS.issubset(result.keys())
        and result["status"] in INFERENCE_STATUSES
    )


def handle_evaluate(speed, distance) -> dict:
    """Điều phối quá trình kiểm tra dữ liệu và suy luận cảnh báo va chạm.

    Args:
        speed: Tốc độ phương tiện (km/h) nhận từ giao diện (thường là str).
        distance: Khoảng cách đến vật cản (m) nhận từ giao diện (thường là str).

    Returns:
        dict gồm 5 trường:
            - status (str): "SAFE" | "WARNING" | "DANGER" | "ERROR"
            - message (str)
            - recommendation (str)
            - rule_id (str | None): R01..R04, hoặc None nếu ERROR
            - d_min (float | None): mét, hoặc None nếu ERROR
    """
    try:
        # Bước 1: Validation (TV3)
        validation_result = validate_input(speed, distance)

        if not isinstance(validation_result, dict):
            return _error_result(
                "Kết quả kiểm tra dữ liệu không đúng định dạng.",
                SYSTEM_ERROR_RECOMMENDATION,
            )

        # Bước 2: Dữ liệu không hợp lệ -> ERROR, dừng, không gọi Inference
        if validation_result.get("valid") is not True:
            error_msg = validation_result.get("error") or DEFAULT_VALIDATION_MESSAGE
            return _error_result(error_msg, DEFAULT_ERROR_RECOMMENDATION)

        # Bước 3: Dùng giá trị đã được Validation chuẩn hóa (float)
        clean_speed = validation_result["speed"]
        clean_distance = validation_result["distance"]

        inference_result = evaluate_collision(clean_speed, clean_distance)

        # Bước 4: Kiểm tra cấu trúc, rồi giữ nguyên kết quả khi chuyển về giao diện
        if not _is_valid_inference_result(inference_result):
            return _error_result(
                "Kết quả suy luận không đầy đủ hoặc không đúng định dạng.",
                SYSTEM_ERROR_RECOMMENDATION,
            )

        return inference_result

    except Exception as exc:  # lỗi bất ngờ từ module phía sau: không để hệ thống sập
        return _error_result(
            f"Đã xảy ra lỗi hệ thống trong quá trình xử lý: {exc}",
            SYSTEM_ERROR_RECOMMENDATION,
        )


def main():
    """Điểm khởi chạy chương trình."""
    # Import trễ để việc test handle_evaluate không phụ thuộc tkinter / môi trường hiển thị.
    from src.interface import run_app

    run_app(handle_evaluate)


if __name__ == "__main__":
    main()
