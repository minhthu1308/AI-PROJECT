# KẾT QUẢ KIỂM THỬ
## Dự án: Hệ thống cảnh báo va chạm

## 1. Thông tin chạy test

- Lệnh: `python -m pytest tests/ -v -ra`
- Python: 3.13.5
- pytest: 9.0.2
- Bộ test: `tests/`
- Test data: `tests/test_data/test_cases.csv`

## 2. Kết quả tổng hợp

**Kết quả: 104 PASS, 0 FAIL, 0 SKIP.**

| Nhóm | Nội dung | Kết quả |
|---|---|---:|
| Validation | Kiểm tra dữ liệu đầu vào | PASS |
| Inference | `calculate_d_min()` và `evaluate_collision()` | PASS |
| Integration | `handle_evaluate()` + Validation + Inference | PASS |
| Exception handling | Ngoại lệ và kết quả sai cấu trúc | PASS |
| Boundary cases | Các mốc tốc độ/khoảng cách | PASS |
| Special values | NaN, Infinity, None, whitespace, Boolean | PASS |

## 3. Phạm vi test case chính

Source hiện tại có **TC01-TC30**.

- TC01-TC18: trường hợp hợp lệ và giá trị biên.
- TC19-TC30: trường hợp dữ liệu không hợp lệ.

Tất cả các trường hợp tích hợp tương ứng đều PASS.

## 4. Các điểm đã kiểm tra

### Validation

- Tốc độ 0-120 km/h.
- Tốc độ âm.
- Tốc độ vượt 120 km/h.
- Khoảng cách âm.
- Chuỗi không hợp lệ.
- Chuỗi rỗng/khoảng trắng.
- `None`.
- NaN/Infinity.
- Boolean.
- Chuỗi số hợp lệ được chuẩn hóa thành `float`.

### Inference

- R01: `0, 0` -> DANGER.
- R02: khoảng cách nhỏ hơn D_min -> DANGER.
- R03: trong khoảng D_min đến D_min + 10 -> WARNING.
- R04: lớn hơn D_min + 10 -> SAFE.
- D_min đúng tại các mốc 60, 80, 100 và 120 km/h.
- D_min là `float` và được so sánh bằng `pytest.approx()`.
- Kết quả có đủ 5 trường bắt buộc.

### Integration

- Validation chạy trước Inference.
- Input không hợp lệ không gọi Inference.
- Input hợp lệ truyền `float` đã chuẩn hóa sang Inference.
- Kết quả Inference được giữ nguyên khi chuyển tiếp.
- Lỗi từ Validation/Inference được chuyển thành `ERROR`.
- Kết quả Validation/Inference sai cấu trúc được phát hiện.

## 5. Đánh giá

**PASS toàn bộ bộ kiểm thử.**

Không phát hiện lỗi trong phạm vi các chức năng và hợp đồng module được kiểm thử bằng source hiện tại.

## 6. Ghi chú

Kết quả này phản ánh source tại thời điểm kiểm thử. Nếu TV3, TV4 hoặc TV5 thay đổi logic, cấu trúc dữ liệu hoặc module contract, cần chạy lại toàn bộ bộ test và cập nhật tài liệu kết quả.
## 7. Minh chứng kiểm thử

Kết quả kiểm thử được thực hiện bằng pytest.

- Tổng số: 104 PASS, 0 FAIL, 0 SKIP.
- Phiên bản Python: 3.13.5.
- Phiên bản pytest: 9.2.0.
- Commit kiểm thử: `9f56ea609f060b32e4007fe10c7d9d1a9c82a185`.
