# TÀI LIỆU KIỂM THỬ HỆ THỐNG
## Dự án: Mô phỏng cảnh báo nguy cơ va chạm phương tiện

## 1. GIỚI THIỆU
### 1.1. Mục đích:
Tài liệu này mô tả kế hoạch, phạm vi, dữ liệu và phương pháp kiểm thử cho hệ thống mô phỏng cảnh báo va chạm phương tiện. 

Mục tiêu của kiểm thử:
- Kiểm tra tính hợp lệ của dữ liệu đầu vào.
- Kiểm tra kết quả tính toán khoảng cách an toàn tối thiểu (D_min).
- Kiểm tra khả năng phân loai mức độ nguy hiểm.
- Kiểm tra mã luật IF-THEN được áp dụng.
- Kiểm tra kết quả trả về giữa các module.
- Phát hiện và ghi nhận lỗi trong quá trình phát triển. 

## 2. PHẠM VI KIỂM THỬ
### 2.1. Kiểm thử validation

Hàm được kiểm thử: `validate_input(speed, distance)`

Các nội dung kiểm thử:
- Kiểm tra dữ liệu đầu vào cso bị bỏ trống hay không
- Kiểm tra khả năng chuyển đổi dữ liệu dang kiểu số
- Kiểm tra giá trị âm
- Kiểm tra NaN và Infinity
- Kiểm tra cấu trúc kết quả trả về 

### 2.2. Kiểm thử Inference

Hàm được kiểm thử:
- `calculate_d_min(speed)`
- `evaluate_collision(speed, distance)`

Các nội dung:
- Kiểm tra giá trị D_min tại các mốc tốc độ
- Kiểm tra giá trị biên của các ngưỡng.
- Kiểm tra kết quả SAFE, WARNING và DANGER
- Kiểm tra mã luật R01, R02, R03 và R04
- Kiểm tra đầy đủ các trường trong kết quả trả về

### 2.3. Kiểm thử tích hợp

Kiểm tra luồng xử lý:

UI → Main → Validation → Inference → Main → UI 

Các nội dung:
- Dữ liệu hợp lệ được chuyển đến Inference
- Dữ liệu không hợp lệ không được chuyển đến Inference
- Kết quả từ Inference được Main chuyển tiếp chính xác
- UI nhận và hiển thị đầy đủ thông tin kết quả 

## 3. MÔI TRƯỜNG KIỂM THỬ
| Thành phần | Phiên bản/Công cụ |
|---|---|
| Hệ điều hành | Windows |
| Ngôn ngữ lập trình | Python |
| Python | 3.13.5 |
| Framework kiểm thử | pytest |
| pytest | 9.2.0 |
| Công cụ phát triển | VS Code |
| Quản lý mã nguồn | Git và Github |

## 4. QUY TẮC GIAO TIẾP GIỮA CÁC MODULE

### 4.1. Hàm Validation

Tên hàm:

`validate_input(speed, distance)`

Kết quả hợp lệ:

```Python 
{
    "valid": True,
    "speed": 60.0,
    "distance": 30.0,
    "error": None
}
```

Kết quả không hợp lệ:

```Python 
{
    "valid": False,
    "speed": None,
    "distance": None,
    "error": "Invalid speed value."
}
```

Các trường bắt buộc:

| Trường | Ý nghĩa 
|---|---|
| valid | Trạng thái hợp lệ của dữ liệu |
| speed | Tốc độ sau khi chuyển đổi |
| distance | Khoảng cách sau khi chuyển đổi |
| error | Thông báo lỗi nếu dữ liệu không hợp lệ |

## 4.2. Hàm calculate_d_min

Tên hàm:

`calculate_d_min(speed)`

Quy định:

- Kiểu trả về: float.

- Đơn vị: mét (m).

- Trả về một giá trị D_min, không trả về dictionary.

- Không làm tròn giá trị trước khi sử dụng để phân loại.

- Với speed = 0, trả về 0.0.

- Chỉ tính toán trong phạm vi tốc độ được hỗ trợ: 0-120km/h.

## 4.3. Hàm evaluate_collision

Tên hàm:

`evaluate_collision(speed, distance)`

Kết quả trả về phải có đủ năm trường bắt buộc:

```Python 
{
    "status": "WARNING",
    "message": "Có nguy cơ va chạm.",
    "recommendation": "Hãy thận trọng và chủ động xử lý.",
    "rule_id": "R03",
    "d_min": 35.0
}
```

| Trường | Ý nghĩa |
|---|---|
| status | Kết quả phân loại |
| message | Thông báo kết quả |
| recommendation | Khuyến nghị xử lý |
| rule_id | Mã luật được áp dụng |
| d_min | Khoảng cách an toàn tối thiểu |

## 5. CƠ SỞ XÂY DỰNG TEST DATA

### 5.1. Các ngưỡng D_min

| Khoảng tốc độ (km/h) | Công thức / D_min |
|---|---|
| 0 ≤ V < 60 | D_min = 35 × V / 60 |
| V = 60 | 35 m | 
| 60 < V ≤ 80 | 55 m |
| 80 < V ≤ 100 | 70 m |
| 100 < V ≤ 120 | 100 m |

### 5.2. Ngưỡng phân loại trạng thái

Với khoảng cách thực tế d, khoảng cách tối thiểu D_min và khoảng cảnh báo Δ = 10 m:

| Điều kiện | Kết quả | Mã luật | 
|---|---|---|
| d < D_min | DANGER | R02 |
| D_min ≤ d ≤ D_min + 10 | WARNING | R03 |
| d > D_min + 10 | SAFE | R04 |

Trường hợp đặc biệt:

| Điều kiện | Kết quả | Mã luật |
| speed = 0 và distance = 0 | DANGER | R01 | 

Với speed = 0 và distance > 0, D_min = 0; việc phân loại được thực hiện theo các ngưỡng R03 và R04.

### 5.3. Thứ tự xử lý

1. Kiểm tra dữ liệu đầu vào.

2. Nếu dữ liệu không hợp lệ hoặc speed > 120: trả ERROR và dừng suy luận.

3. Kiểm tra R01.

4. Nếu R01 không kích hoạt, kiểm tra R02.

5. Nếu R02 không kích hoạt, kiểm tra R03.

6. Nếu R03 không kích hoạt, áp dụng R04.

## 6. DANH SÁCH TEST CASE

`tests/test_data/test_cases.csv`

Các trường dữ liệu:

- test_id: mã kiểm thử.

- speed: tốc độ đầu vào.

- distance: khoảng cách đầu vào.

- expected_status: trạng thái mong đợi.

- expected_rule: mã luật mong đợi.

- expected_d_min: khoảng cách an toàn tối thiểu mong đợi.

### 6.1. Nhóm kiểm thử phân loại trạng thái

| Test ID | Speed | Distance | Expected Status | Expected Rule | D_min |
|---|---|---|---|---|---|
| TC01 | 0 | 0 | DANGER | R01 | 0 |
| TC02 | 0 | 5 | WARNING | R03| 0 |
| TC03 | 0 | 10 | WARNING | R03 | 0 |
| TC04 | 0 | 10.01 | SAFE | R04 | 0 |
| TC05 | 30 | 17.49 | DANGER | R02 | 17.5 |
| TC06 | 30 | 17.5 | WARNING | R03 | 17.5 |
| TC07 | 30 | 27.5 | WARNING |  R03 | 17.5 |
| TC08 | 30 | 27.51 | SAFE | R04 | 17.5 |
| TC09 | 59.99 | 34.99 | DANGER | R02 | 34.994167 |
| TC10 | 60 | 34.99 | DANGER | R02 | 35 | 
| TC11 | 60 | 35 | WARNING | R03 | 35 |
| TC12 | 60 | 45 | WARNING | R03 | 35 |
| TC13 | 60 | 45.01 | SAFE | R04 | 35 |
| TC14 | 80 | 55 | WARNING | R03 | 55 |
| TC15 | v80.01 | 69.99 | DANGER | R02 | 70 |
| TC16 | 100 | 80 | WARNING | R03 | 70 |
| TC17 | 100.01 | 99.99 | DANGER | R02 | 100 |
| TC18 | 120 | 110 | WARNING | R03 | 100 | 

### 6.2. Nhóm kiểm thử dữ liệu không hợp lệ

| Test ID | Speed | Distance | Expected Status | Nội dung |
|---|---|----|---|---|
| TC19 | 120.01 | 110 | ERROR | Tốc độ vượt giới hạn |
| TC20 | -1 | 10 | ERROR | Tốc độ âm |
| TC21 | 40 | -0.1 | ERROR | Khoảng cách âm |
| TC22 | abc | 10 | ERROR | Tốc độ không phải số |
| TC23 | 40 | NaN | ERROR | Khoảng cách NaN |
| TC24 | 40 | Infinity | ERROR | Khoảng cách vô cực 
| TC25 | Trống | 10 | ERROR | Thiếu tốc độ |
| TC26 | 40 | Trống | ERROR | Thiếu khoảng cách |

### 6.3. Kiểm thử bổ sung

Ngoài 26 trường hợp chính thức, TV2 có thể bổ sung các trường hợp:

- Tốc độ NaN.

- Tốc độ Infinity.

- Khoảng cách nhập chữ.

- Dữ liệu đầu vào dạng chuỗi số hợp lệ, ví dụ "60" và "30".

- Chuỗi rỗng "" ở từng trường.
