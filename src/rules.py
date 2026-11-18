MAX_SPEED = 120.0   
DELTA = 10.0        

RULES = {
    "R01": {
        "status": "DANGER",
        "message": "có khả năng phương tiện đã xảy ra va chạm",
        "recommendation": "kiểm tra tình trạng phương tiện và khoảng cách với vật thể phía trước",
    },
    "R02": {
        "status": "DANGER",
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
        "message": "Khoảng cách an toàn.",
        "recommendation": "Tiếp tục duy trì khoảng cách.",
    },
}
