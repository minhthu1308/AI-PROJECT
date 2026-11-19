from src.validation import validate_input
from src.inference import evaluate_collision


# Năm trường bắt buộc của kết quả evaluate_collision().
REQUIRED_FIELDS = frozenset({"status", "message", "recommendation", "rule_id", "d_min"})

# Ba trạng thái hợp lệ do Inference Engine trả về.
INFERENCE_STATUSES = frozenset({"SAFE", "WARNING", "DANGER"})

DEFAULT_VALIDATION_MESSAGE = "Dữ liệu đầu vào không hợp lệ."
DEFAULT_ERROR_RECOMMENDATION = (
    "Vui lòng kiểm tra và nhập lại tốc độ (0 - 120 km/h) "
    "và khoảng cách (>= 0 m) hợp lệ."
)
SYSTEM_ERROR_RECOMMENDATION = "Vui lòng thử lại hoặc liên hệ nhóm phát triển."


def _error_result(message, recommendation) -> dict:
    """Tạo kết quả ERROR khi dữ liệu không hợp lệ hoặc có lỗi hệ thống."""
    return {
        "status": "ERROR",
        "message": message,
        "recommendation": recommendation,
        "rule_id": None,
        "d_min": None,
    }


def _is_valid_inference_result(result) -> bool:
    """Kiểm tra cấu trúc kết quả trả về từ Inference Engine."""
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
        # Bước 1: Kiểm tra tính hợp lệ của dữ liệu đầu vào
        validation_result = validate_input(speed, distance)

        if not isinstance(validation_result, dict):
            return _error_result(
                "Kết quả kiểm tra dữ liệu không đúng định dạng.",
                SYSTEM_ERROR_RECOMMENDATION,
            )

        # Bước 2: Trả về ERROR nếu dữ liệu không hợp lệ, không gọi Inference
        if validation_result.get("valid") is not True:
            error_msg = validation_result.get("error") or DEFAULT_VALIDATION_MESSAGE
            return _error_result(error_msg, DEFAULT_ERROR_RECOMMENDATION)

        # Bước 3: Gọi suy luận với giá trị đã chuẩn hóa (float)
        clean_speed = validation_result["speed"]
        clean_distance = validation_result["distance"]

        inference_result = evaluate_collision(clean_speed, clean_distance)

        # Bước 4: Kiểm tra cấu trúc kết quả trước khi trả về giao diện
        if not _is_valid_inference_result(inference_result):
            return _error_result(
                "Kết quả suy luận không đầy đủ hoặc không đúng định dạng.",
                SYSTEM_ERROR_RECOMMENDATION,
            )

        return inference_result

    except Exception as exc:
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
