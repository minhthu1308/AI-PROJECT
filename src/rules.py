"""Định nghĩa luật IF-THEN R01-R04.

Nguồn: tài liệu kiểm thử của TV2 (mục 5.2, 5.3). Cần TV1 xác nhận lại,
đặc biệt là nội dung message / recommendation (đánh dấu TODO).
"""

MAX_SPEED = 120.0   # km/h, vượt quá là ERROR
DELTA = 10.0        # khoảng cảnh báo (m)

RULES = {
    "R01": {
        "status": "DANGER",
        # TODO: xác nhận nội dung với TV1
        "message": "Phương tiện đang va chạm.",
        "recommendation": "Khuyến nghị xử lý ngay.",
    },
    "R02": {
        "status": "DANGER",
        # TODO: xác nhận nội dung với TV1
        "message": "Khoảng cách nhỏ hơn khoảng cách an toàn tối thiểu.",
        "recommendation": "Giảm tốc độ và tăng khoảng cách ngay.",
    },
    "R03": {
        "status": "WARNING",
        "message": "Có nguy cơ va chạm.",
        "recommendation": "Hãy thận trọng và chủ động xử lý.",
    },
    "R04": {
        "status": "SAFE",
        # TODO: xác nhận nội dung với TV1
        "message": "Khoảng cách an toàn.",
        "recommendation": "Tiếp tục duy trì khoảng cách.",
    },
}
