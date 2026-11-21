# TÀI LIỆU KIỂM THỬ HỆ THỐNG
## Dự án: Mô phỏng cảnh báo nguy cơ va chạm phương tiện

## 1. GIỚI THIỆU
### 1.1. Mục đích:
Tài liệu này mô tả phạm vi, phương pháp, dữ liệu và tiêu chí đánh giá hoạt động kiểm thử đối với hệ thống mô phỏng cảnh báo nguy cơ va chạm phương tiện.

Hệ thống sử dụng phương pháp suy luận dựa trên luật (Rule-Based Reasoning), tiếp nhận hai thông số đầu vào gồm tốc độ phương tiện và khoảng cách đến vật cản. Dựa trên dữ liệu hợp lệ, hệ thống tính toán khoảng cách an toàn tối thiểu và áp dụng các luật IF–THEN để phân loại trạng thái cảnh báo.

Hoạt động kiểm thử nhằm xác minh rằng các chức năng xử lý dữ liệu, tính toán, suy luận và điều phối giữa các module hoạt động phù hợp với đặc tả đã thống nhất.

### 1.2. Mục tiêu kiểm thử

Các mục tiêu kiểm thử bao gồm:

- Xác minh tính hợp lệ và khả năng chuẩn hóa dữ liệu đầu vào.

- Kiểm tra công thức tính khoảng cách an toàn tối thiểu (D_min).

- Xác minh kết quả phân loại theo bốn luật R01–R04.

- Kiểm tra các trường hợp tại giá trị biên và dữ liệu không hợp lệ.

- Kiểm tra cấu trúc dữ liệu trả về của các module.

- Xác minh thứ tự điều phối giữa Validation và Inference.

- Kiểm tra khả năng xử lý ngoại lệ và kết quả sai cấu trúc.

- Đảm bảo dữ liệu không hợp lệ không được chuyển vào bộ suy luận.

### 1.3. Phân loại kiểm thử

Bộ kiểm thử được tổ chức thành hai nhóm chính:

**Unit Testing**: Kiểm thử độc lập các chức năng trong module Validation và Inference.

**Integration Testing**: Kiểm thử quá trình điều phối và giao tiếp giữa Main Controller, Validation và Inference, thông qua hàm **handle_evaluate()**.

Các trường hợp kiểm thử được xây dựng dựa trên mã nguồn, quy định giao tiếp giữa các module và tập dữ liệu được lưu trong **tests/test_data/test_cases.csv**.

### 1.4. Giới hạn phạm vi

Bộ kiểm thử tự động hiện tại tập trung vào logic xử lý và giao tiếp giữa các module Python.

Kiểm thử tương tác trực tiếp với giao diện Tkinter cần được thực hiện và ghi nhận riêng. Kết quả kiểm thử tự động không được xem là bằng chứng đầy đủ cho toàn bộ hành vi giao diện người dùng.

## 2. Phạm vi kiểm thử

Hoạt động kiểm thử tự động tập trung vào ba thành phần chính của hệ thống: **Input Validation**, **Inference Engine** và **Main Controller**.

Bộ kiểm thử sử dụng framework `pytest` nhằm xác minh tính chính xác của từng chức năng và khả năng phối hợp giữa các module.

### 2.1. Kiểm thử Input Validation

**Module:** `src/validation.py`  
**File kiểm thử:** `tests/test_validation.py`  
**Hàm được kiểm thử:** `validate_input(speed, distance)`

Mục tiêu của nhóm kiểm thử này là xác minh dữ liệu đầu vào được kiểm tra và chuẩn hóa đúng trước khi chuyển sang bộ suy luận.

Các trường hợp kiểm thử bao gồm:

- **Dữ liệu hợp lệ:** Tốc độ trong phạm vi từ 0 đến 120 km/h và khoảng cách không âm.
- **Dữ liệu ngoài phạm vi:** Tốc độ âm, tốc độ vượt 120 km/h hoặc khoảng cách âm.
- **Dữ liệu sai định dạng:** Chuỗi không thể chuyển đổi thành số.
- **Dữ liệu rỗng:** Chuỗi rỗng hoặc chuỗi chỉ chứa khoảng trắng.
- **Giá trị đặc biệt:** `None`, `NaN`, `Infinity` và Boolean (`True`, `False`).
- **Chuẩn hóa dữ liệu:** Chuỗi biểu diễn số hợp lệ được chuyển thành kiểu `float`.
- **Cấu trúc kết quả:** Kiểm tra các trường bắt buộc `valid`, `speed`, `distance` và `error`.

Đối với dữ liệu hợp lệ, hàm phải trả về `valid = True`, trong đó tốc độ và khoảng cách đã được chuẩn hóa.

Đối với dữ liệu không hợp lệ, hàm phải trả về `valid = False`, hai trường `speed` và `distance` có giá trị `None`, đồng thời cung cấp thông báo lỗi.

### 2.2. Kiểm thử Inference Engine

**Module:** `src/inference.py`  
**File kiểm thử:** `tests/test_inference.py`

Các hàm được kiểm thử:

- `calculate_d_min(speed)`
- `evaluate_collision(speed, distance)`

#### 2.2.1. Kiểm thử tính toán khoảng cách an toàn tối thiểu

Hàm `calculate_d_min()` được kiểm tra nhằm xác minh kết quả tính toán phù hợp với công thức và các khoảng tốc độ đã quy định.

Các giá trị được kiểm tra gồm:

| Tốc độ (km/h) | D_min mong đợi (m) |
|---|---|
| 0 | 0 |
| 30 | 17.5 |
| 59.99 | 35 × 59.99 / 60 |
| 60 | 35 |
| 80 | 55 |
| 80.01 | 70 |
| 100 | 70 |
| 100.01 | 100 |
| 120 | 100 |

Các bài kiểm thử xác minh:

- Kết quả tính toán đúng với giá trị mong đợi.
- Giá trị trả về thuộc kiểu `float`.
- Sử dụng `pytest.approx()` để so sánh số thực.
- Các ngưỡng tốc độ được phân chia đúng theo đặc tả.

#### 2.2.2. Kiểm thử luật suy luận IF–THEN

Hàm `evaluate_collision()` được kiểm thử để xác minh khả năng phân loại trạng thái dựa trên các luật R01–R04.

| Luật | Nội dung kiểm thử | Kết quả mong đợi |
|---|---|---|
| R01 | Tốc độ và khoảng cách cùng bằng 0 | DANGER |
| R02 | Khoảng cách nhỏ hơn D_min | DANGER |
| R03 | Khoảng cách nằm trong đoạn từ D_min đến D_min + 10 | WARNING |
| R04 | Khoảng cách lớn hơn D_min + 10 | SAFE |

Bên cạnh việc xác minh trạng thái và mã luật, bộ kiểm thử còn kiểm tra cấu trúc kết quả gồm năm trường bắt buộc:

- `status`
- `message`
- `recommendation`
- `rule_id`
- `d_min`

Trong đó, `message` và `recommendation` phải là chuỗi không rỗng, còn `d_min` phải thuộc kiểu `float` và có giá trị phù hợp với công thức.

### 2.3. Kiểm thử Main Controller và tích hợp module

**Module:** `src/main.py`  
**File kiểm thử:** `tests/test_main.py`  
**Hàm được kiểm thử:** `handle_evaluate(speed, distance)`

Mục tiêu của nhóm kiểm thử này là xác minh Main Controller điều phối đúng quá trình kiểm tra dữ liệu, suy luận và xử lý kết quả.

#### 2.3.1. Kiểm thử điều phối bằng Mock

Bộ kiểm thử sử dụng `unittest.mock` để mô phỏng kết quả và ngoại lệ phát sinh từ các module.

Các nội dung được kiểm tra:

- Validation được gọi với dữ liệu đầu vào ban đầu.
- Khi Validation trả về dữ liệu không hợp lệ, Main trả về `ERROR` và không gọi Inference.
- Khi Validation trả về dữ liệu hợp lệ, Main truyền các giá trị đã chuẩn hóa sang Inference.
- Khi Inference trả về kết quả hợp lệ, Main chuyển tiếp kết quả mà không thay đổi nội dung.
- Khi Validation không cung cấp thông báo lỗi, Main sử dụng thông báo mặc định.

Bộ kiểm thử cũng mô phỏng các tình huống bất thường:

- Validation phát sinh exception.
- Inference phát sinh exception.
- Validation trả về kết quả không phải dictionary hoặc không xác nhận dữ liệu hợp lệ.
- Inference trả về kết quả thiếu trường bắt buộc.
- Inference trả về trạng thái không thuộc `SAFE`, `WARNING`, `DANGER`.
- Inference trả về dữ liệu không phải dictionary.

Các trường hợp này nhằm xác minh Main có thể trả kết quả `ERROR` theo các điều kiện xử lý hiện tại, thay vì để ngoại lệ lan ra từ `handle_evaluate()`.

#### 2.3.2. Kiểm thử tích hợp với module thực

Ngoài Mock Testing, bộ kiểm thử còn gọi trực tiếp `handle_evaluate()` để thực hiện luồng tích hợp giữa Main, Validation và Inference.

Luồng xử lý được kiểm tra:

```text
Input (speed, distance)
        |
        v
Main Controller
        |
        v
Input Validation
        |
        +--- Không hợp lệ ---> ERROR
        |
        v
Inference Engine
        |
        v
Main Controller
        |
        v
Kết quả đánh giá
```

Các trường hợp kiểm thử bao gồm:

- Dữ liệu hợp lệ tương ứng TC01–TC18.
- Dữ liệu không hợp lệ tương ứng TC19–TC30.
- Các trường hợp bổ sung về dữ liệu rỗng và không hữu hạn.
- Khả năng xử lý đầu vào dạng chuỗi số.
- Khả năng xử lý đầu vào dạng `int` hoặc `float`.

Kết quả được kiểm tra thông qua các trường `status`, `rule_id`, `d_min`, `message` và `recommendation`.

### 2.4. Phạm vi chưa được kiểm thử tự động

Bộ kiểm thử hiện tại chưa thực hiện kiểm thử tự động đầy đủ đối với tương tác trực tiếp trên giao diện Tkinter.

Cụ thể, các bài kiểm thử `test_main.py` tập trung vào hàm `handle_evaluate()` và các module xử lý phía sau, không trực tiếp mô phỏng thao tác nhập liệu, nhấn nút hoặc kiểm tra kết quả hiển thị trên cửa sổ ứng dụng.

Vì vậy, việc đánh giá giao diện thực tế cần có hoạt động kiểm thử thủ công và minh chứng riêng.

Ngoài ra, kiểm thử hiện tại xác minh tính đúng đắn của chương trình so với các luật và ngưỡng đã thiết kế, không đánh giá khả năng dự đoán va chạm trong điều kiện giao thông thực tế.

## 3. Môi trường và công cụ kiểm thử

### 3.1. Môi trường kiểm thử

Hệ thống được phát triển bằng ngôn ngữ Python và sử dụng framework `pytest` để thực hiện các bài kiểm thử tự động.

Môi trường được ghi nhận trong tài liệu kiểm thử của nhóm gồm:

| Thành phần | Công nghệ / Phiên bản |
|---|---|
| Hệ điều hành | Windows |
| Ngôn ngữ lập trình | Python |
| Phiên bản Python | 3.13.5 |
| Framework kiểm thử | pytest |
| Công cụ phát triển | Visual Studio Code |
| Quản lý mã nguồn | Git và GitHub |
| Công cụ hỗ trợ Mock Testing | `unittest.mock` |
| Nguồn dữ liệu kiểm thử | Bộ test Python và `tests/test_data/test_cases.csv` |

### 3.2. Công cụ và phương pháp hỗ trợ

#### 3.2.1. pytest

`pytest` là framework được sử dụng để tổ chức và thực thi các bài kiểm thử tự động.

Trong dự án, pytest hỗ trợ:

- Phát hiện và thực thi các hàm kiểm thử.
- Chạy nhiều bộ dữ liệu đầu vào bằng `@pytest.mark.parametrize`.
- Sử dụng các câu lệnh `assert` để xác minh kết quả.
- So sánh số thực thông qua `pytest.approx()`.
- Tổng hợp số lượng kiểm thử thành công, thất bại và bị bỏ qua.
- Chạy toàn bộ bộ kiểm thử hoặc từng file riêng biệt.

#### 3.2.2. unittest.mock

Thư viện `unittest.mock` thuộc thư viện chuẩn Python được sử dụng để mô phỏng hành vi của các module trong quá trình kiểm thử Main Controller.

Thông qua `patch.object()`, bộ kiểm thử có thể thay thế tạm thời kết quả hoặc hành vi của Validation và Inference nhằm xác minh:

- Thứ tự và số lần gọi hàm.
- Việc truyền tham số giữa các module.
- Cách xử lý khi module trả về dữ liệu không hợp lệ.
- Cách xử lý khi module phát sinh ngoại lệ.
- Việc ngăn Inference thực thi khi Validation thất bại.

Mock Testing cho phép kiểm tra riêng trách nhiệm điều phối của Main Controller mà không phụ thuộc hoàn toàn vào kết quả xử lý thực tế của các module phía sau.

#### 3.2.3. Bộ dữ liệu kiểm thử

Bộ dữ liệu tham chiếu được lưu tại:

`tests/test_data/test_cases.csv`

File CSV định nghĩa các trường hợp kiểm thử TC01–TC30, bao gồm dữ liệu đầu vào, kết quả mong đợi và nội dung kiểm tra.

Trong phiên bản hiện tại, các bài kiểm thử Python sử dụng dữ liệu được khai báo trực tiếp trong mã nguồn, chẳng hạn thông qua `@pytest.mark.parametrize`. File CSV đóng vai trò làm nguồn dữ liệu tham chiếu để đối chiếu và quản lý test case.

Vì vậy, khi thay đổi các trường hợp kiểm thử, cần cập nhật đồng bộ file CSV và các bài test tương ứng.

### 3.3. Cấu trúc bộ kiểm thử

Bộ kiểm thử tự động được tổ chức trong thư mục `tests/`:

```text
tests/
├── test_validation.py
├── test_inference.py
├── test_main.py
└── test_data/
    └── test_cases.csv
```

Chức năng của từng file:

| File | Vai trò |
|---|---|
| `test_validation.py` | Kiểm thử khả năng kiểm tra và chuẩn hóa dữ liệu đầu vào |
| `test_inference.py` | Kiểm thử công thức D_min và các luật suy luận R01–R04 |
| `test_main.py` | Kiểm thử điều phối, xử lý ngoại lệ và tích hợp giữa các module |
| `test_cases.csv` | Lưu bộ dữ liệu tham chiếu và kết quả mong đợi |

Việc phân chia này giúp các thành viên có thể kiểm thử độc lập từng chức năng, đồng thời thực hiện kiểm thử tích hợp sau khi các module được hoàn thành.

### 3.4. Quản lý phiên bản và tính tái lập

Mã nguồn và tài liệu kiểm thử được quản lý thông qua Git và GitHub.

Mỗi lần kiểm thử phục vụ nghiệm thu cần ghi nhận phiên bản mã nguồn bằng commit SHA để bảo đảm kết quả có thể được đối chiếu với đúng phiên bản đã kiểm tra.

Khi mã nguồn hoặc bộ kiểm thử thay đổi, nhóm cần chạy lại các bài kiểm thử liên quan trước khi sử dụng kết quả để nghiệm thu.

Các thông tin về kết quả thực thi, số lượng PASS/FAIL/SKIP và bằng chứng kiểm thử được quản lý trong `docs/test_results.md` cùng thư mục `docs/evidence/`.

## 4. Quy tắc dữ liệu và hợp đồng giao tiếp giữa các module

### 4.1. Quy định dữ liệu đầu vào

Hệ thống tiếp nhận hai thông số đầu vào gồm tốc độ phương tiện (`speed`) và khoảng cách đến vật cản (`distance`).

| Tham số | Ý nghĩa | Đơn vị | Điều kiện hợp lệ |
|---|---|---|---|
| `speed` | Tốc độ phương tiện | km/h | 0 ≤ speed ≤ 120 |
| `distance` | Khoảng cách đến vật cản | m | distance ≥ 0 |

Dữ liệu phải có khả năng chuyển đổi thành số thực hữu hạn (`float`).

Các trường hợp không hợp lệ bao gồm:

- Giá trị âm hoặc vượt phạm vi cho phép.
- Chuỗi rỗng hoặc chỉ chứa khoảng trắng.
- Chuỗi không thể chuyển đổi thành số.
- Giá trị `None`.
- Giá trị `NaN` hoặc `Infinity`.
- Giá trị Boolean (`True`, `False`).

Dữ liệu không hợp lệ phải được phát hiện tại bước Validation và không được chuyển sang Inference Engine trong luồng xử lý chính.

### 4.2. Hợp đồng của Input Validation

**Module:** `src/validation.py`  
**Hàm:** `validate_input(speed, distance)`

Hàm có trách nhiệm kiểm tra tính hợp lệ và chuẩn hóa dữ liệu đầu vào.

Kết quả trả về là một dictionary gồm bốn trường bắt buộc:

| Trường | Kiểu dữ liệu | Ý nghĩa |
|---|---|---|
| `valid` | bool | Xác định dữ liệu hợp lệ hay không |
| `speed` | float hoặc None | Tốc độ sau khi chuẩn hóa |
| `distance` | float hoặc None | Khoảng cách sau khi chuẩn hóa |
| `error` | str hoặc None | Thông báo lỗi |

**Trường hợp dữ liệu hợp lệ:**

```python
{
    "valid": True,
    "speed": 60.0,
    "distance": 35.0,
    "error": None
}
```

**Trường hợp dữ liệu không hợp lệ:**

```python
{
    "valid": False,
    "speed": None,
    "distance": None,
    "error": "invalid speed value."
}
```

Bộ kiểm thử cần xác minh rằng kết quả trả về đáp ứng đúng cấu trúc và nội dung tương ứng với từng loại dữ liệu đầu vào.

### 4.3. Hợp đồng của Inference Engine

**Module:** `src/inference.py`

#### 4.3.1. Hàm calculate_d_min()

Hàm `calculate_d_min(speed)` tiếp nhận tốc độ hợp lệ và trả về khoảng cách an toàn tối thiểu theo mô hình.

Các yêu cầu cần kiểm thử:

- Giá trị trả về có kiểu `float`.
- Đơn vị đo là mét (m).
- Công thức tính phù hợp với từng khoảng tốc độ.
- Không làm tròn kết quả trước khi so sánh với các ngưỡng phân loại.
- Với tốc độ bằng 0, kết quả phải bằng `0.0`.
- Với tốc độ ngoài phạm vi hỗ trợ, hàm phát sinh `ValueError`.

Công thức chi tiết được quy định trong `docs/rule_specification.md`.

#### 4.3.2. Hàm evaluate_collision()

Hàm `evaluate_collision(speed, distance)` thực hiện suy luận dựa trên dữ liệu đã được xác nhận hợp lệ và các luật R01–R04.

Hàm trả về một dictionary gồm năm trường bắt buộc:

| Trường | Kiểu dữ liệu | Ý nghĩa |
|---|---|---|
| `status` | str | Trạng thái SAFE, WARNING hoặc DANGER |
| `message` | str | Thông báo giải thích kết quả |
| `recommendation` | str | Khuyến nghị tương ứng |
| `rule_id` | str | Mã luật R01–R04 được áp dụng |
| `d_min` | float | Khoảng cách an toàn tối thiểu |

**Ví dụ kết quả:**

```python
{
    "status": "WARNING",
    "message": "Có nguy cơ va chạm.",
    "recommendation": "Hãy thận trọng và chủ động xử lý.",
    "rule_id": "R03",
    "d_min": 35.0
}
```

Các yêu cầu kiểm thử bao gồm:

- Kết quả phải là dictionary.
- Có đầy đủ năm trường bắt buộc.
- `status` và `rule_id` phù hợp với luật được kích hoạt.
- `d_min` có giá trị và kiểu dữ liệu chính xác.
- `message` và `recommendation` là chuỗi không rỗng.

### 4.4. Hợp đồng của Main Controller

**Module:** `src/main.py`  
**Hàm:** `handle_evaluate(speed, distance)`

Main Controller đóng vai trò điều phối, không trực tiếp thực hiện kiểm tra dữ liệu hoặc tính toán luật suy luận.

Quy trình xử lý:

1. Tiếp nhận dữ liệu đầu vào.
2. Gọi `validate_input()` để kiểm tra tính hợp lệ.
3. Nếu dữ liệu không hợp lệ, trả kết quả `ERROR` mà không gọi Inference.
4. Nếu hợp lệ, truyền dữ liệu đã chuẩn hóa sang `evaluate_collision()`.
5. Kiểm tra cấu trúc kết quả suy luận.
6. Chuyển tiếp kết quả hợp lệ cho giao diện.

Main Controller cũng xử lý các ngoại lệ phát sinh từ các module và chuyển thành kết quả lỗi.

**Cấu trúc kết quả ERROR:**

```python
{
    "status": "ERROR",
    "message": "Dữ liệu đầu vào không hợp lệ.",
    "recommendation": "Vui lòng kiểm tra và nhập lại dữ liệu.",
    "rule_id": None,
    "d_min": None
}
```

Ví dụ trên minh họa cấu trúc kết quả. Nội dung `message` và `recommendation` thực tế phụ thuộc vào nguyên nhân lỗi và cách xử lý của Main.

Các yêu cầu kiểm thử:

- Validation được thực hiện trước Inference.
- Dữ liệu không hợp lệ không được chuyển đến Inference.
- Dữ liệu hợp lệ được chuyển tiếp sau khi chuẩn hóa.
- Kết quả suy luận hợp lệ được giữ nguyên.
- Kết quả sai cấu trúc được xử lý theo các điều kiện kiểm tra hiện tại của Main.
- Ngoại lệ từ các module được chuyển thành kết quả `ERROR`.

### 4.5. Quy định chung về kết quả kiểm thử

Đối với từng chức năng, kết quả thực tế phải được đối chiếu với các điều kiện mong đợi tương ứng.

Việc kiểm tra bao gồm:

- Giá trị trả về.
- Kiểu dữ liệu.
- Cấu trúc dictionary.
- Trạng thái phân loại.
- Mã luật được áp dụng.
- Thứ tự gọi module khi cần thiết.
- Cách xử lý dữ liệu không hợp lệ và ngoại lệ.

Các bài kiểm thử phải dựa trên hợp đồng module và các luật đã được thống nhất, không tự ý thay đổi kết quả mong đợi để phù hợp với hành vi sai của chương trình.

**Tài liệu tham chiếu:**

- `docs/module_contracts.md`: Quy định giao tiếp và trách nhiệm giữa các module.
- `docs/rule_specification.md`: Đặc tả công thức, ngưỡng và luật suy luận R01–R04.
- `tests/test_validation.py`: Kiểm thử Input Validation.
- `tests/test_inference.py`: Kiểm thử Inference Engine.
- `tests/test_main.py`: Kiểm thử Main Controller và tích hợp.

## 5. Cơ sở xây dựng dữ liệu kiểm thử

### 5.1. Nguyên tắc xây dựng test case

Bộ dữ liệu kiểm thử được xây dựng dựa trên đặc tả đầu vào, công thức tính khoảng cách an toàn tối thiểu (`D_min`) và các luật suy luận R01–R04.

Các trường hợp kiểm thử được lựa chọn nhằm kiểm tra cả dữ liệu hợp lệ, dữ liệu không hợp lệ và những giá trị tại vị trí có khả năng làm thay đổi kết quả phân loại.

Ba phương pháp chính được áp dụng gồm:

**a. Phân vùng tương đương (Equivalence Partitioning)**

Phương pháp này chia dữ liệu đầu vào thành những nhóm có cùng đặc điểm xử lý, từ đó lựa chọn các giá trị đại diện để kiểm thử.

Đối với hệ thống, các nhóm dữ liệu chính gồm:

| Nhóm dữ liệu | Điều kiện | Kết quả mong đợi |
|---|---|---|
| Tốc độ hợp lệ | 0 ≤ speed ≤ 120 | Được Validation chấp nhận nếu khoảng cách hợp lệ |
| Tốc độ không hợp lệ | speed < 0 hoặc speed > 120 | ERROR |
| Khoảng cách hợp lệ | distance ≥ 0 | Được Validation chấp nhận nếu tốc độ hợp lệ |
| Khoảng cách không hợp lệ | distance < 0 | ERROR |
| Dữ liệu không thể chuyển thành số hữu hạn | Chuỗi không hợp lệ, NaN, Infinity, None, Boolean | ERROR |
| Khoảng cách dưới ngưỡng | distance < D_min | DANGER / R02 |
| Khoảng cách thuộc vùng cảnh báo | D_min ≤ distance ≤ D_min + 10 | WARNING / R03 |
| Khoảng cách vượt vùng cảnh báo | distance > D_min + 10 | SAFE / R04 |

Trường hợp `speed = 0` và `distance = 0` được kiểm thử riêng theo luật đặc biệt R01, có độ ưu tiên cao hơn các luật phân loại khoảng cách.

**b. Phân tích giá trị biên (Boundary Value Analysis)**

Phương pháp này tập trung vào các giá trị tại, ngay dưới và ngay trên những ngưỡng có thể làm thay đổi kết quả xử lý.

Trong hệ thống, các ngưỡng tốc độ cần kiểm tra gồm:

| Mốc tốc độ | Trường hợp kiểm thử | Ý nghĩa |
|---|---|---|
| 0 km/h | speed = 0 | Kiểm tra giới hạn dưới và trường hợp đặc biệt R01 |
| 60 km/h | 59.99 và 60 | Kiểm tra khoảng tính D_min đầu tiên |
| 80 km/h | 80 và 80.01 | Kiểm tra chuyển từ D_min = 55 sang 70 |
| 100 km/h | 100 và 100.01 | Kiểm tra chuyển từ D_min = 70 sang 100 |
| 120 km/h | 120 và 120.01 | Kiểm tra giới hạn trên của tốc độ hợp lệ |

Ngoài các ngưỡng tốc độ, bộ kiểm thử còn tập trung vào hai ngưỡng khoảng cách:

- `distance = D_min`: Biên giữa DANGER và WARNING.
- `distance = D_min + 10`: Biên trên của WARNING.

Các giá trị ngay dưới hoặc ngay trên hai ngưỡng này được sử dụng để kiểm tra việc áp dụng chính xác các toán tử so sánh `<`, `<=` và `>` trong bộ suy luận.

**c. Kiểm thử dữ liệu không hợp lệ (Negative Testing)**

Negative Testing được sử dụng để xác minh hệ thống từ chối dữ liệu không đáp ứng điều kiện đầu vào.

Các nhóm dữ liệu được kiểm tra bao gồm:

- Tốc độ âm hoặc vượt 120 km/h.
- Khoảng cách âm.
- Chuỗi ký tự không thể chuyển thành số.
- Chuỗi rỗng hoặc chỉ chứa khoảng trắng.
- Giá trị NaN và Infinity.
- Giá trị None hoặc Boolean trong các bài kiểm thử Python.

Đối với những trường hợp này, kết quả mong đợi từ `handle_evaluate()` là `ERROR`, đồng thời Inference Engine không được thực thi sau khi Validation xác định dữ liệu không hợp lệ.

### 5.2. Cơ sở tính toán kết quả mong đợi

Đối với dữ liệu đầu vào hợp lệ, kết quả mong đợi được xác định bằng cách tính `D_min` từ tốc độ và áp dụng các luật suy luận theo đúng thứ tự.

Công thức tính `D_min` được quy định như sau:

| Khoảng tốc độ V (km/h) | D_min (m) |
|---|---|
| 0 ≤ V ≤ 60 | 35 × V / 60 |
| 60 < V ≤ 80 | 55 |
| 80 < V ≤ 100 | 70 |
| 100 < V ≤ 120 | 100 |

Với khoảng cảnh báo bổ sung `DELTA = 10 m`, các điều kiện phân loại được xác định như sau:

| Mã luật | Điều kiện | Kết quả |
|---|---|---|
| R01 | speed = 0 và distance = 0 | DANGER |
| R02 | Không thuộc R01 và distance < D_min | DANGER |
| R03 | Không thuộc R01/R02 và D_min ≤ distance ≤ D_min + 10 | WARNING |
| R04 | distance > D_min + 10 | SAFE |

Các luật được xét theo thứ tự R01 → R02 → R03 → R04 để bảo đảm trường hợp đặc biệt được xử lý trước các điều kiện thông thường.

Các công thức và điều kiện này là quy tắc của mô hình mô phỏng, không phải kết quả đánh giá độ an toàn thực tế ngoài môi trường giao thông.

### 5.3. Ví dụ thiết kế test case theo giá trị biên

Xét trường hợp tốc độ phương tiện bằng 30 km/h.

Khoảng cách tối thiểu được tính:

`D_min = 35 × 30 / 60 = 17.5 m`

Khoảng cảnh báo trên:

`D_min + DELTA = 17.5 + 10 = 27.5 m`

Từ đó xây dựng các trường hợp:

| Test case | Speed | Distance | Kết quả mong đợi | Mục đích |
|---|---:|---:|---|---|
| TC05 | 30 | 17.49 | DANGER / R02 | Ngay dưới D_min |
| TC06 | 30 | 17.5 | WARNING / R03 | Đúng D_min |
| TC07 | 30 | 27.5 | WARNING / R03 | Đúng biên trên WARNING |
| TC08 | 30 | 27.51 | SAFE / R04 | Ngay trên biên WARNING |

Các trường hợp trên giúp xác minh sự thay đổi trạng thái khi khoảng cách đi qua các ngưỡng đã xác định.

### 5.4. Phân nhóm bộ dữ liệu kiểm thử

Bộ dữ liệu tham chiếu được lưu tại `tests/test_data/test_cases.csv`, gồm 30 trường hợp được đánh số từ TC01 đến TC30.

| Nhóm | Test case | Nội dung |
|---|---|---|
| Trường hợp đặc biệt khi speed = 0 | TC01–TC04 | Kiểm tra R01, R03, R04 |
| Kiểm thử biên khoảng cách tại speed = 30 | TC05–TC08 | Kiểm tra R02, R03, R04 |
| Kiểm thử các mốc tốc độ và khoảng cách | TC09–TC18 | Kiểm tra D_min, R02, R03, R04 |
| Tốc độ hoặc khoảng cách ngoài phạm vi | TC19–TC21 | Kiểm tra Validation |
| Dữ liệu sai định dạng, rỗng, NaN, Infinity | TC22–TC30 | Kiểm tra Validation |

Trong đó:

- **TC01–TC18:** Là những trường hợp đầu vào hợp lệ, phục vụ kiểm tra giá trị D_min và kết quả suy luận.
- **TC19–TC30:** Là những trường hợp đầu vào không hợp lệ, phục vụ kiểm tra việc từ chối dữ liệu.

Ngoài bộ dữ liệu tham chiếu TC01–TC30, các file kiểm thử Python còn chứa các trường hợp bổ sung về kiểu dữ liệu và tình huống giao tiếp bất thường giữa các module.

### 5.5. Quy tắc quản lý và đồng bộ test data

Các test case trong `test_cases.csv` được sử dụng làm dữ liệu tham chiếu cho quá trình kiểm thử.

Trong phiên bản hiện tại, dữ liệu kiểm thử được khai báo trực tiếp trong các file Python bằng `@pytest.mark.parametrize`, thay vì được pytest đọc trực tiếp từ CSV.

Vì vậy, khi điều chỉnh công thức D_min, tập luật hoặc kết quả mong đợi, nhóm cần đồng bộ:

- `tests/test_data/test_cases.csv`
- `tests/test_validation.py`
- `tests/test_inference.py`
- `tests/test_main.py`
- `docs/rule_specification.md`
- `docs/test_documentation.md`

Việc thay đổi kết quả mong đợi phải dựa trên đặc tả đã được thống nhất và được review trước khi hợp nhất mã nguồn.

Chi tiết từng trường hợp TC01–TC30 được trình bày tại Mục 6 của tài liệu này.

## 6. Danh sách test case

### 6.1. Tổng quan bộ dữ liệu kiểm thử

Bộ dữ liệu kiểm thử được lưu tại:

`tests/test_data/test_cases.csv`

File gồm 30 trường hợp kiểm thử, được đánh số từ TC01 đến TC30 và chia thành hai nhóm:

- **TC01–TC18:** Kiểm thử dữ liệu hợp lệ, công thức tính `D_min`, luật suy luận R01–R04 và các giá trị biên.
- **TC19–TC30:** Kiểm thử dữ liệu không hợp lệ và khả năng từ chối dữ liệu của Validation.

Cấu trúc file CSV gồm các trường:

| Trường | Ý nghĩa |
|---|---|
| `test_id` | Mã định danh test case |
| `speed` | Tốc độ đầu vào (km/h) |
| `distance` | Khoảng cách đầu vào (m) |
| `expected_d_min` | Giá trị khoảng cách tối thiểu mong đợi |
| `expected_status` | Trạng thái mong đợi |
| `expected_rule` | Mã luật hoặc nhóm xử lý mong đợi |
| `test_category` | Nhóm kiểm thử |
| `explanation` | Giải thích mục đích kiểm thử |

Đối với các trường hợp dữ liệu không hợp lệ, `expected_d_min` được ghi là `N/A` do hệ thống không thực hiện suy luận. Trường `expected_rule` được ghi là `Validation` để thể hiện bước từ chối dữ liệu, không phải một mã luật suy luận R01–R04.

### 6.2. Nhóm kiểm thử dữ liệu hợp lệ và giá trị biên

Bảng sau mô tả các trường hợp TC01–TC18 nhằm xác minh kết quả tính toán và phân loại trạng thái.

| Test ID | Speed (km/h) | Distance (m) | D_min (m) | Expected Status | Expected Rule |
|---|---:|---:|---:|---|---|
| TC01 | 0 | 0 | 0 | DANGER | R01 |
| TC02 | 0 | 5 | 0 | WARNING | R03 |
| TC03 | 0 | 10 | 0 | WARNING | R03 |
| TC04 | 0 | 10.01 | 0 | SAFE | R04 |
| TC05 | 30 | 17.49 | 17.5 | DANGER | R02 |
| TC06 | 30 | 17.5 | 17.5 | WARNING | R03 |
| TC07 | 30 | 27.5 | 17.5 | WARNING | R03 |
| TC08 | 30 | 27.51 | 17.5 | SAFE | R04 |
| TC09 | 59.99 | 34.99 | ≈34.994167 | DANGER | R02 |
| TC10 | 60 | 34.99 | 35 | DANGER | R02 |
| TC11 | 60 | 35 | 35 | WARNING | R03 |
| TC12 | 60 | 45 | 35 | WARNING | R03 |
| TC13 | 60 | 45.01 | 35 | SAFE | R04 |
| TC14 | 80 | 55 | 55 | WARNING | R03 |
| TC15 | 80.01 | 69.99 | 70 | DANGER | R02 |
| TC16 | 100 | 80 | 70 | WARNING | R03 |
| TC17 | 100.01 | 99.99 | 100 | DANGER | R02 |
| TC18 | 120 | 110 | 100 | WARNING | R03 |

**Phân tích các nhóm trường hợp:**

**TC01–TC04 — Tốc độ bằng 0**

Nhóm này xác minh cách xử lý khi tốc độ phương tiện bằng 0.

- TC01 kiểm tra luật đặc biệt R01 khi tốc độ và khoảng cách cùng bằng 0.
- TC02–TC03 kiểm tra vùng cảnh báo R03 khi `D_min = 0`.
- TC04 kiểm tra trạng thái SAFE khi khoảng cách lớn hơn `D_min + 10`.

**TC05–TC08 — Giá trị biên tại tốc độ 30 km/h**

Nhóm này kiểm tra khả năng chuyển đổi trạng thái khi khoảng cách đi qua ngưỡng `D_min = 17.5 m` và `D_min + 10 = 27.5 m`.

- TC05: Ngay dưới ngưỡng tối thiểu.
- TC06: Đúng ngưỡng tối thiểu.
- TC07: Đúng biên trên của vùng cảnh báo.
- TC08: Ngay trên biên cảnh báo.

**TC09–TC13 — Ngưỡng tốc độ 60 km/h**

Nhóm này kiểm tra công thức tính khoảng cách tối thiểu khi tốc độ tiến đến và bằng 60 km/h, đồng thời xác minh các điều kiện phân loại R02, R03 và R04.

**TC14–TC18 — Các mốc tốc độ cao**

Các trường hợp này tập trung kiểm tra sự thay đổi của `D_min` tại các ngưỡng 80, 100 và 120 km/h.

Đặc biệt:

- TC15 kiểm tra ngay trên mốc 80 km/h, khi `D_min` chuyển từ 55 m sang 70 m.
- TC17 kiểm tra ngay trên mốc 100 km/h, khi `D_min` chuyển từ 70 m sang 100 m.
- TC18 kiểm tra giới hạn trên 120 km/h của phạm vi được hỗ trợ.

### 6.3. Nhóm kiểm thử dữ liệu không hợp lệ

Các trường hợp TC19–TC30 nhằm xác minh hệ thống phát hiện và từ chối những dữ liệu không đáp ứng quy định đầu vào.

| Test ID | Speed | Distance | Expected Status | Nội dung kiểm thử |
|---|---|---|---|---|
| TC19 | 120.01 | 110 | ERROR | Tốc độ vượt giới hạn |
| TC20 | -1 | 10 | ERROR | Tốc độ âm |
| TC21 | 40 | -0.1 | ERROR | Khoảng cách âm |
| TC22 | abc | 10 | ERROR | Tốc độ không phải số |
| TC23 | 40 | NaN | ERROR | Khoảng cách NaN |
| TC24 | 40 | Infinity | ERROR | Khoảng cách vô cực |
| TC25 | Trống | 10 | ERROR | Thiếu tốc độ |
| TC26 | 40 | Trống | ERROR | Thiếu khoảng cách |
| TC27 | NaN | 10 | ERROR | Tốc độ NaN |
| TC28 | Infinity | 10 | ERROR | Tốc độ vô cực |
| TC29 | 40 | abc | ERROR | Khoảng cách không phải số |
| TC30 | Khoảng trắng | 10 | ERROR | Tốc độ chỉ chứa khoảng trắng |

Đối với những trường hợp này, hệ thống phải:

1. Phát hiện dữ liệu không hợp lệ tại bước Validation.
2. Không thực hiện suy luận dựa trên các luật R01–R04.
3. Trả về trạng thái `ERROR` thông qua Main Controller.
4. Không cung cấp `rule_id` hoặc `d_min` cho kết quả lỗi.

Khi Main Controller tạo kết quả `ERROR`, hai trường `rule_id` và `d_min` có giá trị `None`.

### 6.4. Các trường hợp kiểm thử bổ sung trong mã nguồn

Ngoài TC01–TC30, các file kiểm thử Python còn sử dụng những bộ dữ liệu và tình huống bổ sung.

**a. Các trường hợp bổ sung cho Validation**

- Giá trị `None` ở từng trường.
- Giá trị Boolean (`True`, `False`).
- Chuỗi số hợp lệ cần chuẩn hóa thành `float`.
- Giá trị NaN và Infinity dưới dạng số hoặc chuỗi.
- Chuỗi rỗng và chuỗi khoảng trắng.
- Cấu trúc dictionary của kết quả Validation.

**b. Các trường hợp bổ sung cho Inference**

- Kiểm tra giá trị `D_min` tại nhiều mốc tốc độ.
- Xác minh kiểu dữ liệu `float` của `d_min`.
- Kiểm tra cấu trúc kết quả suy luận.
- Xác minh thông báo và khuyến nghị là chuỗi không rỗng.

**c. Các trường hợp bổ sung cho Main Controller**

Bộ kiểm thử sử dụng `unittest.mock` để kiểm tra các tình huống:

- Validation trả về dữ liệu không hợp lệ.
- Validation không cung cấp nội dung lỗi.
- Inference trả về kết quả thiếu trường bắt buộc.
- Inference trả về trạng thái không hợp lệ.
- Validation hoặc Inference trả về dữ liệu không đúng dạng.
- Validation hoặc Inference phát sinh ngoại lệ.
- Main chuyển tiếp kết quả hợp lệ mà không thay đổi nội dung.
- Main truyền dữ liệu đã chuẩn hóa sang Inference.

Các trường hợp này giúp bổ sung phạm vi kiểm thử ngoài những tình huống đầu vào được biểu diễn trong CSV.

### 6.5. Quan hệ giữa test case và số lượng bài kiểm thử

Cần phân biệt giữa **test case trong CSV** và **test instance được pytest thực thi**.

File `test_cases.csv` chứa 30 trường hợp tham chiếu. Trong khi đó, số lượng test được pytest thực thi có thể lớn hơn 30 vì:

- Một test case có thể được kiểm tra ở nhiều cấp độ khác nhau.
- Các file Python sử dụng `@pytest.mark.parametrize` để thực thi nhiều bộ dữ liệu.
- Bộ kiểm thử còn bao gồm kiểm tra cấu trúc, kiểu dữ liệu, xử lý ngoại lệ và Mock Testing.

Các file test Python hiện khai báo bộ dữ liệu trực tiếp trong mã nguồn, không đọc CSV tự động trong quá trình chạy.

Vì vậy, số lượng test PASS/FAIL/SKIP và kết quả thực thi thực tế được ghi nhận riêng trong `docs/test_results.md`.

### 6.6. Nguyên tắc đồng bộ dữ liệu kiểm thử

Khi có thay đổi đối với công thức `D_min`, các luật R01–R04 hoặc hợp đồng giữa các module, nhóm cần:

1. Xác định những test case bị ảnh hưởng.
2. Đối chiếu và cập nhật kết quả mong đợi trong CSV.
3. Điều chỉnh các bài kiểm thử Python tương ứng.
4. Chạy lại các bài kiểm thử liên quan và toàn bộ bộ test khi tích hợp.
5. Cập nhật tài liệu và minh chứng thực thi nếu có thay đổi.

Việc đồng bộ giữa dữ liệu tham chiếu, mã nguồn kiểm thử và tài liệu nhằm bảo đảm tính nhất quán và khả năng truy vết trong quá trình phát triển.

## 7. Phương pháp kiểm thử và tiêu chí PASS/FAIL

### 7.1. Phương pháp thực hiện kiểm thử

Bộ kiểm thử của hệ thống được xây dựng bằng framework `pytest`, sử dụng các câu lệnh `assert` để so sánh kết quả thực tế với kết quả mong đợi.

Các phương pháp kiểm thử chính bao gồm Unit Testing, Integration Testing và Mock Testing.

#### 7.1.1. Unit Testing

Unit Testing được sử dụng để kiểm tra các hàm xử lý độc lập trong hai module:

- `src/validation.py`
- `src/inference.py`

Đối với Validation, các bài kiểm thử xác minh khả năng tiếp nhận, kiểm tra và chuẩn hóa dữ liệu đầu vào.

Đối với Inference, các bài kiểm thử xác minh công thức tính `D_min`, việc áp dụng các luật R01–R04 và cấu trúc kết quả suy luận.

Mỗi bài kiểm thử thực hiện theo nguyên tắc:

1. Xác định dữ liệu đầu vào.
2. Xác định kết quả mong đợi theo đặc tả.
3. Gọi hàm cần kiểm thử.
4. So sánh kết quả thực tế với kết quả mong đợi.
5. Ghi nhận PASS hoặc FAIL theo kết quả thực thi.

#### 7.1.2. Integration Testing

Integration Testing được sử dụng để kiểm tra khả năng phối hợp giữa Main Controller, Input Validation và Inference Engine.

Hàm được kiểm thử là:

`handle_evaluate(speed, distance)`

Các bài kiểm thử tích hợp sử dụng module thực để xác minh quá trình:

```text
Input
  |
  v
Main Controller
  |
  v
Input Validation
  |
  +--- Không hợp lệ ---> ERROR
  |
  v
Inference Engine
  |
  v
Main Controller
  |
  v
Kết quả đánh giá
```

Những nội dung được kiểm tra gồm:

- Dữ liệu hợp lệ được Validation chấp nhận và chuẩn hóa.
- Dữ liệu đã chuẩn hóa được chuyển đến Inference.
- Inference trả về kết quả phù hợp với luật suy luận.
- Main chuyển tiếp kết quả hợp lệ mà không thay đổi nội dung.
- Dữ liệu không hợp lệ được xử lý thành `ERROR`.

Bộ kiểm thử tích hợp hiện tập trung vào các module xử lý Python, chưa tự động thực hiện thao tác trên cửa sổ Tkinter.

#### 7.1.3. Mock Testing

Mock Testing được sử dụng trong `tests/test_main.py` thông qua thư viện `unittest.mock`.

Phương pháp này cho phép mô phỏng kết quả hoặc ngoại lệ của Validation và Inference để kiểm tra riêng trách nhiệm điều phối của Main Controller.

Các trường hợp kiểm thử bao gồm:

- Validation trả về dữ liệu không hợp lệ.
- Validation không cung cấp thông báo lỗi.
- Validation trả về dữ liệu sai cấu trúc.
- Inference trả về kết quả thiếu trường bắt buộc.
- Inference trả về trạng thái không hợp lệ.
- Validation hoặc Inference phát sinh ngoại lệ.
- Inference không được gọi khi Validation thất bại.
- Kết quả hợp lệ được chuyển tiếp nguyên vẹn.

Mock Testing hỗ trợ xác minh cách Main xử lý các tình huống bất thường mà không cần sửa trực tiếp mã nguồn của Validation hoặc Inference.

### 7.2. Kỹ thuật đối chiếu kết quả

#### 7.2.1. Kiểm tra giá trị bằng assertion

Các bài kiểm thử sử dụng `assert` để xác minh kết quả thực tế.

Ví dụ:

```python
assert result["status"] == "WARNING"
assert result["rule_id"] == "R03"
```

Hai assertion này xác minh trạng thái và mã luật được áp dụng.

#### 7.2.2. So sánh số thực

Các phép tính khoảng cách sử dụng kiểu dữ liệu `float`, vì vậy bộ kiểm thử dùng `pytest.approx()` để so sánh kết quả số thực với giá trị mong đợi trong sai số cho phép.

Ví dụ:

```python
assert result["d_min"] == pytest.approx(expected_d_min)
```

Việc sử dụng `pytest.approx()` giúp tránh các trường hợp FAIL không cần thiết do sai khác rất nhỏ trong biểu diễn số dấu phẩy động.

#### 7.2.3. Kiểm tra kiểu dữ liệu và cấu trúc kết quả

Ngoài kiểm tra giá trị, bộ kiểm thử còn xác minh cấu trúc dữ liệu trả về của các module.

Ví dụ:

```python
assert isinstance(result, dict)
assert {"status", "message", "recommendation", "rule_id", "d_min"}.issubset(result)
```

Các điều kiện này xác minh kết quả là dictionary và chứa đầy đủ các trường bắt buộc.

Bộ kiểm thử Inference còn xác minh:

- `d_min` thuộc kiểu `float`.
- `message` là chuỗi không rỗng.
- `recommendation` là chuỗi không rỗng.

Đối với Validation, các bài kiểm thử kiểm tra các trường `valid`, `speed`, `distance` và `error`.

#### 7.2.4. Kiểm tra hành vi giữa các module

Trong Mock Testing, bộ kiểm thử sử dụng các phương thức của `unittest.mock` để xác minh cách Main gọi các module.

Ví dụ:

```python
mock_val.assert_called_once_with("60", "35")
mock_inf.assert_called_once_with(60.0, 35.0)
```

Các assertion này xác minh Main chuyển dữ liệu ban đầu đến Validation và chuyển dữ liệu đã chuẩn hóa đến Inference.

Đối với dữ liệu không hợp lệ:

```python
mock_inf.assert_not_called()
```

Điều kiện này xác minh Inference không được thực thi khi Validation từ chối dữ liệu.

### 7.3. Tiêu chí PASS

Một bài kiểm thử được xem là **PASS** khi toàn bộ các assertion và điều kiện thực thi của bài kiểm thử đều thành công.

Tùy theo chức năng được kiểm tra, tiêu chí PASS bao gồm:

| Nhóm kiểm thử | Tiêu chí PASS |
|---|---|
| Validation | Xác định đúng dữ liệu hợp lệ hoặc không hợp lệ |
| Chuẩn hóa dữ liệu | Các giá trị hợp lệ được chuyển thành `float` |
| D_min | Kết quả tính toán phù hợp với công thức |
| Inference | Trả đúng trạng thái và mã luật |
| Cấu trúc dữ liệu | Có đầy đủ các trường bắt buộc |
| Kiểu dữ liệu | Các trường được kiểm tra đáp ứng kiểu dữ liệu mong đợi |
| Main Controller | Gọi module đúng theo các tình huống được kiểm thử |
| Xử lý lỗi | Trả về `ERROR` theo điều kiện đã quy định |
| Integration | Kết quả cuối cùng phù hợp với dữ liệu đầu vào và luật suy luận |

Ví dụ, với dữ liệu:

- `speed = 60`
- `distance = 35`

Ta có:

- `D_min = 35 m`
- Luật áp dụng: R03
- Trạng thái mong đợi: WARNING

Bài kiểm thử được xem là PASS nếu các giá trị thực tế đáp ứng những assertion tương ứng.

### 7.4. Tiêu chí FAIL

Một bài kiểm thử được xem là **FAIL** khi ít nhất một điều kiện mong đợi không được đáp ứng.

Các trường hợp FAIL có thể bao gồm:

- Validation chấp nhận dữ liệu không hợp lệ.
- Validation từ chối dữ liệu hợp lệ.
- Giá trị `D_min` không phù hợp với công thức.
- Inference trả sai trạng thái hoặc mã luật.
- Kết quả thiếu trường bắt buộc.
- Kiểu dữ liệu không đáp ứng assertion.
- Main gọi Inference khi Validation đã từ chối dữ liệu.
- Main không xử lý đúng ngoại lệ được mô phỏng.
- Kết quả tích hợp không phù hợp với kết quả mong đợi.

Khi phát hiện FAIL, cần xác định test case liên quan, dữ liệu đầu vào, kết quả thực tế và assertion bị vi phạm để phục vụ quá trình điều tra và sửa lỗi.

### 7.5. Các trạng thái kết quả kiểm thử khác

Ngoài PASS và FAIL, pytest còn có thể ghi nhận các trạng thái khác.

| Trạng thái | Ý nghĩa |
|---|---|
| PASSED | Bài kiểm thử thực hiện thành công |
| FAILED | Có điều kiện kiểm thử không đạt |
| ERROR | Phát sinh lỗi trong quá trình chuẩn bị, thu thập hoặc thực thi kiểm thử |
| SKIPPED | Bài kiểm thử bị bỏ qua |
| XFAILED | Bài kiểm thử được đánh dấu dự kiến thất bại |
| XPASSED | Bài kiểm thử dự kiến thất bại nhưng thực tế lại thành công |

Cần phân biệt **ERROR của pytest** với trạng thái `ERROR` do ứng dụng trả về.

Trong ứng dụng, `ERROR` là một kết quả xử lý dữ liệu hoặc lỗi hệ thống. Một bài kiểm thử hoàn toàn có thể PASS khi xác minh ứng dụng trả về `ERROR` đúng như mong đợi.

Đối với ba file kiểm thử hiện tại, `pytest.importorskip()` được sử dụng trong quá trình import module. Do đó, nếu module cần kiểm thử không thể import, bài kiểm thử có thể bị SKIPPED thay vì FAILED.

Vì vậy, việc nghiệm thu không chỉ dựa vào số lượng PASS mà còn cần kiểm tra các trường hợp SKIPPED hoặc ERROR ngoài dự kiến.

### 7.6. Tiêu chí đánh giá kết quả tổng hợp

Để đánh giá toàn bộ bộ kiểm thử tự động, nhóm sử dụng các tiêu chí:

1. Tất cả bài kiểm thử bắt buộc phải PASS.
2. Không có bài kiểm thử FAILED hoặc ERROR.
3. Không có bài kiểm thử SKIPPED ngoài dự kiến.
4. Kết quả phải tương ứng với phiên bản mã nguồn được ghi nhận.
5. Các test case và kết quả mong đợi phải nhất quán với đặc tả hiện hành.

Kết quả thực thi thực tế, số lượng PASS/FAIL/SKIP và minh chứng tương ứng được lưu trong `docs/test_results.md`.

Việc toàn bộ bộ kiểm thử tự động đạt PASS chứng minh các hành vi đã được kiểm tra đáp ứng assertion của bộ test. Kết quả này không đồng nghĩa với việc mọi chức năng hoặc tình huống sử dụng của hệ thống đã được kiểm chứng đầy đủ.

## 8. Hướng dẫn thực hiện kiểm thử và ghi nhận kết quả

### 8.1. Chuẩn bị môi trường

Trước khi thực hiện kiểm thử, cần bảo đảm máy tính đã cài đặt Python và có mã nguồn dự án.

Các thao tác thực hiện tại thư mục gốc của repository `AI-PROJECT`.

**Bước 1. Kiểm tra phiên bản Python**

```powershell
python --version
```

**Bước 2. Cài đặt các dependency**

```powershell
python -m pip install -r requirements.txt
```

File `requirements.txt` hiện quy định phiên bản pytest trong khoảng:

```text
pytest>=9.0,<10.0
```

**Bước 3. Kiểm tra phiên bản pytest**

```powershell
python -m pytest --version
```

Các phiên bản công cụ thực tế được ghi nhận cùng kết quả kiểm thử để hỗ trợ truy vết và tái lập.

### 8.2. Chạy toàn bộ bộ kiểm thử

Từ thư mục gốc của dự án, thực hiện:

```powershell
python -m pytest tests/ -v -ra
```

Ý nghĩa các thành phần của lệnh:

| Thành phần | Chức năng |
|---|---|
| `python -m pytest` | Chạy framework pytest bằng Python hiện tại |
| `tests/` | Thực thi các bài kiểm thử trong thư mục tests |
| `-v` | Hiển thị chi tiết tên và trạng thái từng test |
| `-ra` | Hiển thị thêm thông tin tóm tắt về các kết quả không PASS |

Lệnh này được sử dụng để chạy toàn bộ ba file kiểm thử:

- `tests/test_validation.py`
- `tests/test_inference.py`
- `tests/test_main.py`

Sau khi hoàn thành, cần kiểm tra phần tổng kết của pytest để xác định số lượng bài kiểm thử PASSED, FAILED, ERROR và SKIPPED.

### 8.3. Chạy kiểm thử theo từng module

Khi cần kiểm tra riêng một chức năng hoặc điều tra lỗi, có thể thực hiện những lệnh sau.

**Kiểm thử Input Validation:**

```powershell
python -m pytest tests/test_validation.py -v
```

**Kiểm thử Inference Engine:**

```powershell
python -m pytest tests/test_inference.py -v
```

**Kiểm thử Main Controller và Integration:**

```powershell
python -m pytest tests/test_main.py -v
```

Việc chạy từng file giúp khoanh vùng lỗi theo module. Tuy nhiên, khi nghiệm thu phiên bản tích hợp, nhóm cần thực hiện lại lệnh kiểm thử tổng hợp ở Mục 8.2.

### 8.4. Ghi nhận kết quả kiểm thử

Kết quả thực thi được quản lý trong:

`docs/test_results.md`

Mỗi lần kiểm thử phục vụ nghiệm thu cần ghi nhận tối thiểu:

| Thông tin | Nội dung cần ghi nhận |
|---|---|
| Ngày thực hiện | Ngày và thời điểm chạy kiểm thử |
| Người thực hiện | Thành viên phụ trách kiểm thử |
| Môi trường | Hệ điều hành, phiên bản Python và pytest |
| Commit SHA | Phiên bản mã nguồn được kiểm thử |
| Lệnh thực hiện | Lệnh pytest đã sử dụng |
| Tổng số test | Số lượng bài kiểm thử được pytest thu thập |
| Kết quả | Số lượng PASSED, FAILED, ERROR và SKIPPED |
| Vấn đề phát hiện | Mô tả lỗi hoặc giới hạn nếu có |
| Minh chứng | Đường dẫn đến ảnh hoặc log kiểm thử |

Có thể xác định commit đang được kiểm thử bằng lệnh:

```powershell
git rev-parse HEAD
```

Commit SHA được sử dụng để đối chiếu kết quả kiểm thử với phiên bản mã nguồn tại thời điểm chạy.

Nếu có thay đổi mã nguồn hoặc bài kiểm thử sau khi ghi nhận kết quả, cần đánh giá tác động và chạy lại các bài kiểm thử liên quan. Khi nghiệm thu phiên bản tích hợp cuối cùng, cần chạy lại toàn bộ bộ kiểm thử.


### 8.5. Xử lý khi kiểm thử không đạt

Khi phát hiện bài kiểm thử FAILED hoặc ERROR ngoài dự kiến, cần thực hiện:

1. Xác định file và bài kiểm thử không đạt.
2. Kiểm tra dữ liệu đầu vào và kết quả mong đợi.
3. Đối chiếu hành vi thực tế với đặc tả hệ thống.
4. Xác định nguyên nhân thuộc mã nguồn, bài kiểm thử, dữ liệu hay môi trường.
5. Thực hiện sửa đổi phù hợp.
6. Chạy lại bài kiểm thử liên quan.
7. Chạy lại toàn bộ bộ kiểm thử trước khi nghiệm thu.
8. Cập nhật kết quả và minh chứng trong `docs/test_results.md`.

---

## 9. Tiêu chí nghiệm thu, giới hạn và quản lý thay đổi

### 9.1. Tiêu chí nghiệm thu bộ kiểm thử

Bộ kiểm thử tự động được xem là đạt yêu cầu nghiệm thu khi đáp ứng các điều kiện sau:

| Mã | Tiêu chí | Điều kiện nghiệm thu |
|---|---|---|
| AC-01 | Tính hợp lệ dữ liệu | Validation xác định đúng dữ liệu hợp lệ và không hợp lệ trong phạm vi kiểm thử |
| AC-02 | Chuẩn hóa dữ liệu | Dữ liệu số hợp lệ được chuẩn hóa theo hợp đồng |
| AC-03 | Tính toán D_min | Kết quả phù hợp với công thức và các mốc tốc độ |
| AC-04 | Luật suy luận | Các luật R01–R04 được áp dụng đúng theo test case |
| AC-05 | Cấu trúc kết quả | Các trường bắt buộc đáp ứng assertion tương ứng |
| AC-06 | Điều phối module | Validation được gọi trước Inference; dữ liệu không hợp lệ không đi vào Inference |
| AC-07 | Xử lý ngoại lệ | Main xử lý đúng các tình huống lỗi được mô phỏng |
| AC-08 | Kiểm thử tích hợp | Kết quả cuối cùng phù hợp với các trường hợp đầu vào được kiểm thử |
| AC-09 | Kết quả thực thi | Không có FAILED, ERROR hoặc SKIPPED ngoài dự kiến |
| AC-10 | Khả năng truy vết | Có thông tin môi trường, commit và bằng chứng thực thi |

Các tiêu chí này áp dụng cho phạm vi bộ kiểm thử tự động đã được xây dựng.

Việc đạt các tiêu chí trên không đồng nghĩa với việc toàn bộ giao diện và mọi tình huống sử dụng thực tế đã được kiểm chứng.

### 9.2. Giới hạn của hoạt động kiểm thử

**a. Giới hạn về giao diện người dùng**

Bộ kiểm thử tự động hiện tại tập trung vào Validation, Inference và Main Controller.

Các bài kiểm thử tích hợp thông qua `handle_evaluate()` chưa trực tiếp kiểm tra thao tác trên giao diện Tkinter như nhập dữ liệu, nhấn nút hoặc quan sát kết quả hiển thị.

Vì vậy, kiểm thử giao diện cần được thực hiện và ghi nhận riêng nếu nhóm muốn nghiệm thu đầy đủ trải nghiệm người dùng.

**b. Giới hạn về phạm vi dữ liệu**

Bộ dữ liệu kiểm thử gồm các trường hợp đã lựa chọn để kiểm tra giá trị hợp lệ, không hợp lệ, giá trị biên và các tình huống bất thường.

Bộ dữ liệu này không bao phủ mọi giá trị hoặc mọi tổ hợp đầu vào có thể phát sinh.

**c. Giới hạn về đặc tả mô hình**

Hệ thống sử dụng tập luật IF–THEN và công thức tính `D_min` được quy định trước.

Kết quả kiểm thử xác nhận rằng chương trình thực hiện phù hợp với các quy tắc đã thiết kế trong phạm vi được kiểm tra.

Các kết quả này không chứng minh mô hình có khả năng dự đoán chính xác va chạm trong điều kiện giao thông thực tế.

**d. Giới hạn về xác minh hợp đồng module**

Các bài kiểm thử hiện tại chủ yếu xác minh những trường dữ liệu, kiểu dữ liệu và điều kiện được thể hiện trong assertion.

Đặc biệt, Main Controller hiện kiểm tra kết quả Inference là dictionary, có đủ các trường bắt buộc và có trạng thái thuộc tập hợp hợp lệ. Việc kiểm tra đầy đủ kiểu dữ liệu của từng trường chưa được triển khai tại tầng Main.

Vì vậy, không nên kết luận rằng bộ kiểm thử đã xác minh mọi ràng buộc có thể có của hợp đồng module.

### 9.3. Nguyên tắc quản lý thay đổi

Trong quá trình phát triển, việc thay đổi mã nguồn có thể ảnh hưởng đến các bài kiểm thử và kết quả mong đợi.

Những thay đổi cần được xem xét bao gồm:

- Điều chỉnh phạm vi tốc độ hoặc quy định dữ liệu đầu vào.
- Thay đổi công thức tính `D_min`.
- Thay đổi khoảng cảnh báo `DELTA`.
- Bổ sung hoặc điều chỉnh các luật R01–R04.
- Thay đổi cấu trúc dữ liệu trả về.
- Thay đổi giao diện hàm giữa các module.
- Thay đổi logic điều phối hoặc xử lý lỗi.

Khi có thay đổi ảnh hưởng đến hành vi hệ thống, nhóm cần:

1. Xác định phạm vi và các test case chịu ảnh hưởng.
2. Đối chiếu với đặc tả đã được thống nhất.
3. Cập nhật mã nguồn và bài kiểm thử liên quan.
4. Đồng bộ dữ liệu tham chiếu trong CSV nếu cần.
5. Chạy lại kiểm thử.
6. Cập nhật tài liệu và kết quả kiểm thử.
7. Thực hiện review trước khi merge vào nhánh chính.

Các thay đổi chỉ liên quan đến comment hoặc định dạng mã nguồn, không làm thay đổi hành vi thực thi, có thể sử dụng lại kết quả kiểm thử trước đó làm bằng chứng tham khảo. Tuy nhiên, cần kiểm tra diff để xác nhận phạm vi thay đổi và chạy lại kiểm thử khi cần nghiệm thu phiên bản cuối cùng.

### 9.4. Phân chia trách nhiệm

Việc quản lý tài liệu và thực hiện kiểm thử được phân chia như sau:

| Vai trò | Trách nhiệm |
|---|---|
| Thành viên phụ trách kiểm thử | Xây dựng và chạy bộ kiểm thử, ghi nhận kết quả, cung cấp bằng chứng |
| Thành viên phụ trách tài liệu | Chuẩn hóa đặc tả, tài liệu kiểm thử và tổng hợp nội dung báo cáo |
| Thành viên phát triển module | Phối hợp xử lý lỗi và cập nhật mã nguồn theo phạm vi phụ trách |
| Người review Pull Request | Đối chiếu thay đổi, kết quả kiểm thử và điều kiện nghiệm thu |

Việc phân chia trách nhiệm giúp duy trì tính nhất quán giữa mã nguồn, bộ kiểm thử và tài liệu.

### 9.5. Tài liệu liên quan

| Tài liệu | Nội dung |
|---|---|
| `docs/module_contracts.md` | Quy định hợp đồng và trách nhiệm giữa các module |
| `docs/rule_specification.md` | Đặc tả cơ sở tri thức, công thức D_min và luật R01–R04 |
| `docs/test_results.md` | Kết quả chạy kiểm thử và minh chứng |
| `tests/test_data/test_cases.csv` | Bộ dữ liệu tham chiếu TC01–TC30 |
| `README.md` | Hướng dẫn cài đặt, chạy chương trình và kiểm thử |

### 9.6. Kết luận

Tài liệu kiểm thử hệ thống đã xác định mục tiêu, phạm vi, phương pháp, dữ liệu và tiêu chí đánh giá đối với ba thành phần chính: Input Validation, Inference Engine và Main Controller.

Bộ kiểm thử được xây dựng nhằm xác minh tính chính xác của việc xử lý dữ liệu đầu vào, tính toán khoảng cách tối thiểu, áp dụng các luật R01–R04 và điều phối giữa các module.

Các kết quả thực thi và bằng chứng tương ứng được quản lý trong `docs/test_results.md`, giúp nhóm theo dõi, đối chiếu và sử dụng khi tổng hợp báo cáo cuối kỳ.

Việc duy trì tính nhất quán giữa mã nguồn, đặc tả, dữ liệu kiểm thử và kết quả thực thi là cơ sở để đánh giá chất lượng hệ thống trong phạm vi mô hình mô phỏng.
