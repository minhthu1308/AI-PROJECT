# QUY ĐỊNH PHỐI HỢP VÀ GIAO TIẾP GIỮA CÁC MODULE


## 1. Giao diện hàm giữa các module

| File | Hàm | Người phụ trách | Chức năng |
|---|---|---|---|
| `validation.py` | `validate_input(speed, distance)` | TV3 | Kiểm tra dữ liệu đầu vào |
| `inference.py` | `calculate_d_min(speed)` | TV3 | Tính khoảng cách tham chiếu |
| `inference.py` | `evaluate_collision(speed, distance)` | TV3 | Suy luận trạng thái cảnh báo |
| `interface.py` | `run_app(on_submit)` | TV4 | Khởi chạy giao diện và gọi callback |
| `main.py` | `handle_evaluate(speed, distance)` | TV5 | Điều phối quá trình xử lý |

## 2. Quy định cấu trúc dữ liệu trả về

### 2.1. Kết quả trả về cho giao diện

Mọi kết quả trả về cho giao diện phải có tối thiểu ba trường:

- `status`: Trạng thái hệ thống.
- `message`: Thông báo giải thích kết quả.
- `recommendation`: Khuyến nghị tương ứng.

Ví dụ:

```python
{
    "status": "WARNING",
    "message": "Có nguy cơ va chạm.",
    "recommendation": "Hãy thận trọng và chủ động xử lý."
}
```

TV3 có thể bổ sung các trường:

- `rule_id`: Mã luật được kích hoạt.
- `d_min`: Khoảng cách tham chiếu.

Tuy nhiên, không được thay đổi tên ba trường chính.

### 2.2. Kết quả của Validation

Hàm `validate_input(speed, distance)` trả về dictionary theo cấu trúc:

Khi hợp lệ:

```python
{
    "valid": True,
    "speed": 60.0,
    "distance": 30.0,
    "error": None
}
```

Khi không hợp lệ:

```python
{
    "valid": False,
    "speed": None,
    "distance": None,
    "error": "Invalid speed value."
}
```

## 3. Nguyên tắc phân chia trách nhiệm

| Công việc | Thành viên chịu trách nhiệm |
|---|---|
| Kiểm tra dữ liệu đầu vào | TV3 |
| Tính D_min | TV3 |
| Xây dựng luật AI | TV3 |
| Thực hiện suy luận | TV3 |
| Thiết kế giao diện | TV4 |
| Nhận dữ liệu từ người dùng | TV4 |
| Hiển thị kết quả | TV4 |
| Điều phối các module | TV5 |
| Tích hợp chương trình | TV5 |
| Xây dựng test data và kết quả kỳ vọng | TV2 |

### 3.1. Quy định dành cho TV3

- Chịu trách nhiệm toàn bộ logic validation và suy luận.
- Không tự ý thay đổi đặc tả IF–THEN đã được thống nhất.
- Đảm bảo các hàm trả về đúng cấu trúc dữ liệu quy định.

### 3.2. Quy định dành cho TV4

- Chỉ xử lý giao diện, nhận dữ liệu và hiển thị kết quả.
- Không tự viết lại công thức tính D_min.
- Không tự xác định SAFE, WARNING hoặc DANGER.
- Không tự triển khai logic validation của TV3.

### 3.3. Quy định dành cho TV5

- Chịu trách nhiệm kết nối các module.
- Gọi hàm validation của TV3 trước khi gọi Inference Engine.
- Không tự viết lại validation hoặc luật AI.
- Trả kết quả về giao diện theo đúng cấu trúc đã thống nhất.

## 4. Quy trình xử lý dữ liệu

1. TV4 nhận tốc độ và khoảng cách từ người dùng.
2. TV4 gọi callback `on_submit(speed, distance)`.
3. TV5 tiếp nhận dữ liệu thông qua `handle_evaluate(speed, distance)`.
4. TV5 gọi `validate_input()` của TV3.
5. Nếu dữ liệu không hợp lệ, trả kết quả `ERROR` về giao diện.
6. Nếu dữ liệu hợp lệ, TV5 gọi `evaluate_collision()`.
7. Inference Engine trả kết quả suy luận.
8. TV5 chuyển kết quả về TV4.
9. TV4 hiển thị trạng thái, thông báo và khuyến nghị.

## 5. Nguyên tắc phối hợp khi lập trình

- Không tự ý thay đổi tên hàm, tên tham số hoặc cấu trúc dữ liệu đã thống nhất.
- Nếu cần thay đổi giao diện hàm, thành viên phụ trách phải thông báo cho các thành viên liên quan trước khi chỉnh sửa.
- Không tự ý chỉnh sửa file do thành viên khác phụ trách.
- Mỗi thành viên phải kiểm tra module độc lập trước khi bàn giao.
- TV5 kiểm tra tính tương thích trước khi tích hợp các module.
- Mọi thay đổi quan trọng phải được cập nhật vào tài liệu này.

