# QUY ĐỊNH PHỐI HỢP VÀ GIAO TIẾP GIỮA CÁC MODULE

## 1. Giao diện hàm giữa các module

| File | Hàm | Người phụ trách | Chức năng |
|---|---|---|---|
| `validation.py` | `validate_input(speed, distance)` | TV3 | Kiểm tra dữ liệu đầu vào |
| `inference.py` | `calculate_d_min(speed)` | TV3 | Tính khoảng cách an toàn tối thiểu |
| `inference.py` | `evaluate_collision(speed, distance)` | TV3 | Suy luận trạng thái cảnh báo |
| `interface.py` | `run_app(on_submit)` | TV4 | Khởi chạy giao diện và gọi callback |
| `main.py` | `handle_evaluate(speed, distance)` | TV5 | Điều phối quá trình xử lý |

### 1.1. Quy định đối với hàm `calculate_d_min(speed)`

**Chức năng:** Tính khoảng cách an toàn tối thiểu dựa trên tốc độ.

Quy định:

- Tham số đầu vào: `speed` (kiểu số, đơn vị km/h).
- Kiểu dữ liệu trả về: `float`.
- Đơn vị giá trị trả về: mét (m).
- Chỉ trả về một giá trị `D_min`, không trả về dictionary.
- Không làm tròn giá trị `D_min` trước khi sử dụng trong quá trình phân loại.
- Hàm chỉ được gọi sau khi dữ liệu đầu vào đã được kiểm tra hợp lệ.
- Với `speed = 0`, hàm trả về `0.0`.
- Với `speed > 120 km/h`, dữ liệu phải được xử lý là `ERROR` tại bước validation, không gọi hàm tính `D_min`.
- Công thức và phạm vi tốc độ áp dụng phải tuân theo đặc tả ngưỡng đã được TV1 xác nhận. Không tự ý đặt thêm ngưỡng hoặc mở rộng phạm vi tính toán.

### 1.2. Quy định đối với hàm `evaluate_collision(speed, distance)`

**Chức năng:** Thực hiện suy luận và phân loại trạng thái cảnh báo dựa trên tốc độ và khoảng cách.

Hàm chỉ nhận dữ liệu đã được kiểm tra hợp lệ và phải trả về một dictionary có đầy đủ 5 trường bắt buộc:

| Trường | Kiểu dữ liệu | Chức năng |
|---|---|---|
| `status` | `str` | Trạng thái cảnh báo: SAFE, WARNING hoặc DANGER |
| `message` | `str` | Thông báo giải thích kết quả |
| `recommendation` | `str` | Khuyến nghị tương ứng với trạng thái |
| `rule_id` | `str` | Mã luật IF–THEN được áp dụng |
| `d_min` | `float` | Khoảng cách an toàn tối thiểu, đơn vị mét |

Quy định:

- `rule_id` phải phản ánh chính xác luật được áp dụng, ví dụ: R01, R02, R03 hoặc R04.
- `d_min` phải chứa giá trị khoảng cách an toàn tối thiểu được tính toán từ `calculate_d_min(speed)`.
- Không được bỏ bất kỳ trường bắt buộc nào trong kết quả trả về.
- Kể cả khi áp dụng luật đặc biệt R01, kết quả vẫn phải có đủ 5 trường.
- Không tự ý thay đổi mã luật hoặc kết quả phân loại đã được TV1 thống nhất.

**Trường hợp đặc biệt R01:**

Khi `speed = 0` và `distance = 0`, kết quả phải có cấu trúc đầy đủ:

```python
{
    "status": "DANGER",
    "message": "Thông báo cảnh báo tương ứng.",
    "recommendation": "Khuyến nghị xử lý tương ứng.",
    "rule_id": "R01",
    "d_min": 0.0
}
```

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

Đối với kết quả từ Inference Engine, TV5 giữ lại hai trường bổ sung:

- `rule_id`: Mã luật được kích hoạt.
- `d_min`: Khoảng cách an toàn tối thiểu.

TV3 phải đảm bảo kết quả của `evaluate_collision()` luôn có đủ 5 trường theo mục 1.2.

TV5 không được thay đổi tên ba trường chính khi chuyển kết quả về giao diện.

### 2.2. Kết quả của Validation

Hàm `validate_input(speed, distance)` trả về dictionary theo cấu trúc:

**Khi hợp lệ:**

```python
{
    "valid": True,
    "speed": 30.0,
    "distance": 20.0,
    "error": None
}
```

**Khi không hợp lệ:**

```python
{
    "valid": False,
    "speed": None,
    "distance": None,
    "error": "Invalid speed value."
}
```

Quy định:

- `valid`: Xác định dữ liệu đầu vào có hợp lệ hay không.
- `speed`: Giá trị tốc độ sau khi kiểm tra.
- `distance`: Giá trị khoảng cách sau khi kiểm tra.
- `error`: Nội dung lỗi nếu dữ liệu không hợp lệ; nếu hợp lệ thì có giá trị `None`.

### 2.3. Quy định xử lý kết quả ERROR

Khi `validate_input()` trả về `valid = False`:

- TV5 không được gọi `evaluate_collision()`.
- TV5 tạo kết quả ERROR để trả về giao diện.
- Kết quả ERROR phải có tối thiểu ba trường chính: `status`, `message`, `recommendation`.

Ví dụ:

```python
{
    "status": "ERROR",
    "message": "Invalid speed value.",
    "recommendation": "Please enter a valid speed."
}
```

Trường hợp này không yêu cầu mã luật R01–R04 hoặc giá trị `d_min`, vì Inference Engine chưa được thực thi.

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
- Đảm bảo `calculate_d_min()` trả về một giá trị `float`, đơn vị mét.
- Đảm bảo `evaluate_collision()` trả về đầy đủ 5 trường bắt buộc.
- Đảm bảo `rule_id` tương ứng với luật thực sự được áp dụng.
- Đảm bảo `d_min` là giá trị được tính toán theo đặc tả.
- Không tự ý thay đổi tên hàm, tên tham số hoặc cấu trúc dữ liệu đã thống nhất.

### 3.2. Quy định dành cho TV4

- Chỉ xử lý giao diện, nhận dữ liệu và hiển thị kết quả.
- Không tự viết lại công thức tính D_min.
- Không tự xác định SAFE, WARNING hoặc DANGER.
- Không tự triển khai logic validation của TV3.
- Nhận kết quả thông qua callback và hiển thị các trường `status`, `message`, `recommendation`.
- Có thể hiển thị thêm `rule_id` và `d_min` nếu giao diện được thiết kế để thể hiện thông tin này.

### 3.3. Quy định dành cho TV5

- Chịu trách nhiệm kết nối các module.
- Gọi hàm validation của TV3 trước khi gọi Inference Engine.
- Nếu validation không hợp lệ, trả kết quả ERROR và không gọi `evaluate_collision()`.
- Nếu validation hợp lệ, sử dụng dữ liệu đã được kiểm tra để gọi `evaluate_collision()`.
- Không tự viết lại validation, công thức D_min hoặc luật AI.
- Giữ nguyên cấu trúc kết quả trả về từ Inference Engine khi chuyển về giao diện.
- Đảm bảo kết quả gửi cho giao diện có tối thiểu ba trường chính theo mục 2.1.

### 3.4. Quy định dành cho TV2

- Xây dựng bộ test data dựa trên đặc tả đầu vào, ngưỡng và luật IF–THEN đã được thống nhất.
- Kiểm thử hàm `calculate_d_min()` về kiểu dữ liệu, đơn vị và giá trị D_min mong đợi.
- Kiểm thử hàm `evaluate_collision()` về trạng thái phân loại, mã luật và giá trị D_min.
- Đảm bảo kiểm tra đầy đủ 5 trường bắt buộc trong kết quả của `evaluate_collision()`.
- Kiểm thử trường hợp đặc biệt R01.
- Kiểm thử các trường hợp dữ liệu hợp lệ, không hợp lệ và các giá trị biên.
- Đối với giá trị số thực, sử dụng phép so sánh có sai số cho phép thay vì yêu cầu bằng tuyệt đối.

## 4. Quy trình xử lý dữ liệu

1. TV4 nhận tốc độ và khoảng cách từ người dùng.
2. TV4 gọi callback `on_submit(speed, distance)`.
3. TV5 tiếp nhận dữ liệu thông qua `handle_evaluate(speed, distance)`.
4. TV5 gọi `validate_input()` của TV3.
5. Nếu dữ liệu không hợp lệ:
   - TV5 nhận thông tin lỗi từ Validation.
   - TV5 tạo kết quả ERROR có đủ ba trường chính.
   - Không gọi `evaluate_collision()`.
6. Nếu dữ liệu hợp lệ:
   - TV5 sử dụng giá trị `speed` và `distance` đã được Validation xác nhận.
   - TV5 gọi `evaluate_collision(speed, distance)`.
7. Inference Engine thực hiện tính toán D_min và suy luận theo luật IF–THEN.
8. Inference Engine trả về dictionary có đủ 5 trường: `status`, `message`, `recommendation`, `rule_id`, `d_min`.
9. TV5 chuyển kết quả về TV4 mà không làm thay đổi tên các trường dữ liệu.
10. TV4 hiển thị trạng thái, thông báo và khuyến nghị cho người dùng.

## 5. Nguyên tắc phối hợp khi lập trình

- Không tự ý thay đổi tên hàm, tên tham số hoặc cấu trúc dữ liệu đã thống nhất.
- Nếu cần thay đổi giao diện hàm, thành viên phụ trách phải thông báo cho các thành viên liên quan trước khi chỉnh sửa.
- Không tự ý chỉnh sửa file do thành viên khác phụ trách.
- Mỗi thành viên phải kiểm tra module độc lập trước khi bàn giao.
- TV5 kiểm tra tính tương thích trước khi tích hợp các module.
- TV2 cập nhật test data khi có thay đổi được nhóm thống nhất trong đặc tả.
- Mọi thay đổi quan trọng phải được cập nhật vào tài liệu này.
- Các thành viên phải sử dụng cùng một phiên bản module contract khi phát triển và tích hợp chương trình.