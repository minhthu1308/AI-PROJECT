
# ĐẶC TẢ CƠ SỞ TRI THỨC VÀ LUẬT SUY LUẬN

**Dự án:** Hệ thống mô phỏng cảnh báo nguy cơ va chạm phương tiện  
**Tài liệu:** `docs/rule_specification.md`  
**Phạm vi đối chiếu:** `src/rules.py`, `src/inference.py`, `src/validation.py`, `src/main.py` trên nhánh `main`

## 1. Mục đích và phạm vi

Tài liệu mô tả các tham số, công thức và luật IF–THEN mà phiên bản hiện tại của hệ thống sử dụng để **phân loại cảnh báo từ hai giá trị đầu vào**: tốc độ phương tiện và khoảng cách đến vật cản. Đây là đặc tả cho **mô hình mô phỏng dựa trên luật**, không phải thuật toán phát hiện va chạm đã được kiểm chứng trong điều kiện giao thông thực tế.

Hệ thống không học luật từ dữ liệu. Các ngưỡng và nội dung cảnh báo được cấu hình cố định trong mã nguồn. Tài liệu này phục vụ đối chiếu code, xây dựng test case và tổng hợp báo cáo; chi tiết hợp đồng giao tiếp giữa các module được trình bày tại `docs/module_contracts.md`.

## 2. Thành phần cơ sở tri thức

| Thành phần | Vị trí trong mã nguồn | Vai trò |
|---|---|---|
| Tham số mô hình | `src/rules.py` | `MAX_SPEED = 120.0` (km/h), `DELTA = 10.0` (m) |
| Tập thông tin luật | `src/rules.py` (`RULES`) | Ánh xạ mã R01–R04 sang `status`, `message`, `recommendation` |
| Công thức khoảng cách tối thiểu | `src/inference.py` (`calculate_d_min`) | Tính `D_min` từ tốc độ |
| Điều kiện và thứ tự kích hoạt luật | `src/inference.py` (`evaluate_collision`) | Chọn luật R01, R02, R03 hoặc R04 |
| Kiểm tra dữ liệu đầu vào | `src/validation.py` (`validate_input`) | Xác nhận phạm vi và chuẩn hóa dữ liệu trước khi suy luận |
| Điều phối và xử lý lỗi | `src/main.py` (`handle_evaluate`) | Chỉ gọi Inference khi Validation hợp lệ; trả `ERROR` khi cần |

**Lưu ý:** Ở bản hiện tại, các điều kiện IF–THEN *không* được lưu trực tiếp trong từ điển `RULES`. Tập luật logic được triển khai bằng các nhánh điều kiện trong `evaluate_collision()`, còn `RULES` lưu thông tin kết quả ứng với từng mã luật.

## 3. Dữ liệu đầu vào và ký hiệu

| Ký hiệu / tên | Ý nghĩa | Đơn vị và điều kiện |
|---|---|---|
| `V` / `speed` | Tốc độ đầu vào | km/h; `0 ≤ V ≤ 120` |
| `d` / `distance` | Khoảng cách đến vật cản | m; `d ≥ 0` |
| `D_min` / `d_min` | Khoảng cách tối thiểu theo mô hình | m; được tính từ `V` |
| `DELTA` / `Δ` | Biên cảnh báo bổ sung | `10 m` |
| `MAX_SPEED` | Giới hạn tốc độ được hỗ trợ | `120 km/h` |

`validate_input(speed, distance)` chuyển các đầu vào hợp lệ sang `float`. Chuỗi rỗng, chuỗi chỉ có khoảng trắng, số âm ngoài phạm vi, giá trị không phải số, `None`, Boolean, `NaN` và vô cực bị từ chối theo các điều kiện tương ứng. Chỉ dữ liệu đã được Validation xác nhận mới chuyển tới `evaluate_collision()` trong luồng ứng dụng chính.

## 4. Quy tắc tính khoảng cách tối thiểu

Với tốc độ hợp lệ, `calculate_d_min(V)` trả về giá trị `float` theo công thức phân đoạn:

| Phạm vi tốc độ V (km/h) | D_min (m) |
|---|---|
| `0 ≤ V ≤ 60` | `35 × V / 60` |
| `60 < V ≤ 80` | `55` |
| `80 < V ≤ 100` | `70` |
| `100 < V ≤ 120` | `100` |

Ví dụ: `V = 0` ⇒ `D_min = 0`; `V = 30` ⇒ `17.5 m`; `V = 60` ⇒ `35 m`; `V = 80` ⇒ `55 m`; `V = 100` ⇒ `70 m`; `V = 120` ⇒ `100 m`.

**Quy tắc số học:** Không làm tròn `D_min` trước khi đối chiếu các ngưỡng phân loại. Với `speed` ngoài `[0, 120]`, hàm `calculate_d_min()` chủ động phát sinh `ValueError`; trong luồng UI → Main, trường hợp này được Validation chặn trước.

## 5. Đặc tả luật IF–THEN

Các luật được xét **theo thứ tự**, sau bước Validation và sau khi tính `D_min`.

| Mã | Điều kiện kích hoạt | Trạng thái | Ý nghĩa |
|---|---|---|---|
| **R01** | `V == 0` **và** `d == 0` | `DANGER` | Tình huống đặc biệt: có khả năng phương tiện đã xảy ra va chạm |
| **R02** | Không áp dụng R01 **và** `d < D_min` | `DANGER` | Khoảng cách dưới ngưỡng tối thiểu của mô hình |
| **R03** | Không áp dụng R01/R02 **và** `D_min ≤ d ≤ D_min + DELTA` | `WARNING` | Khoảng cách thuộc vùng cảnh báo, bao gồm hai biên |
| **R04** | `d > D_min + DELTA` | `SAFE` | Khoảng cách vượt biên cảnh báo theo mô hình |

### 5.1. R01 — Trường hợp đặc biệt

**IF** `V == 0 AND d == 0` **THEN** trả `DANGER`, `rule_id = "R01"`, `d_min = 0.0`.

R01 có độ ưu tiên cao nhất để tình huống `(0, 0)` không bị gán sang R03. Thông báo chỉ phản ánh **khả năng**, không khẳng định chắc chắn đã xảy ra va chạm.

### 5.2. R02 — Khoảng cách dưới ngưỡng

**IF** R01 không kích hoạt **AND** `d < D_min` **THEN** trả `DANGER`, `rule_id = "R02"`.

### 5.3. R03 — Vùng cảnh báo

**IF** R01 và R02 không kích hoạt **AND** `d ≤ D_min + 10` **THEN** trả `WARNING`, `rule_id = "R03"`.

Do R02 đã được xét trước, điều kiện thực tế của R03 là `D_min ≤ d ≤ D_min + 10`.

### 5.4. R04 — Vượt vùng cảnh báo

**IF** cả R01, R02 và R03 đều không kích hoạt **THEN** trả `SAFE`, `rule_id = "R04"`.

Với đầu vào hợp lệ, điều kiện này tương đương `d > D_min + 10`.

## 6. Thông báo và khuyến nghị theo mã luật

Bảng sau phản ánh các chuỗi được khai báo trong `src/rules.py` tại thời điểm đối chiếu; không tự ý thay đổi nội dung của mã nguồn khi chỉnh tài liệu.

| Luật | Trạng thái | `message` | `recommendation` |
|---|---|---|---|
| R01 | DANGER | `có khả năng phương tiện đã xảy ra va chạm` | `kiểm tra tình trạng phương tiện và khoảng cách với vật thể phía trước` |
| R02 | DANGER | `Khoảng cách nhỏ hơn khoảng cách an toàn tối thiểu.` | `Giảm tốc độ và tăng khoảng cách ngay.` |
| R03 | WARNING | `Có nguy cơ va chạm.` | `Hãy thận trọng và chủ động xử lý.` |
| R04 | SAFE | `Khoảng cách an toàn.` | `Tiếp tục duy trì khoảng cách.` |

## 7. Kết quả suy luận và xử lý lỗi

`evaluate_collision(speed, distance)` trả một dictionary gồm đúng các trường chính sau:

```python
{
    "status": "WARNING",
    "message": "Có nguy cơ va chạm.",
    "recommendation": "Hãy thận trọng và chủ động xử lý.",
    "rule_id": "R03",
    "d_min": 35.0,
}
```

Ví dụ trên phù hợp với `V = 60 km/h`, `d = 35 m`.

- `status` của kết quả suy luận: `SAFE`, `WARNING` hoặc `DANGER`.
- `rule_id`: một trong `R01`, `R02`, `R03`, `R04`.
- `d_min`: giá trị `float` do mô hình tính toán.
- `message` và `recommendation`: nội dung từ `RULES[rule_id]`.

Trạng thái `ERROR` **không phải là luật R01–R04**. Main tạo `ERROR` nếu Validation từ chối dữ liệu hoặc gặp kết quả/ngoại lệ không xử lý được theo hợp đồng. Khi trả `ERROR`, `rule_id` và `d_min` là `None`.

## 8. Ví dụ và các trường hợp biên

| V (km/h) | d (m) | D_min (m) | Luật | Trạng thái | Ghi chú |
|---:|---:|---:|---|---|---|
| 0 | 0 | 0 | R01 | DANGER | R01 được xét trước |
| 0 | 5 | 0 | R03 | WARNING | Trong vùng `0–10 m` |
| 0 | 10.01 | 0 | R04 | SAFE | Trên `D_min + 10` |
| 30 | 17.49 | 17.5 | R02 | DANGER | Dưới `D_min` |
| 30 | 17.5 | 17.5 | R03 | WARNING | Đúng biên dưới |
| 30 | 27.5 | 17.5 | R03 | WARNING | Đúng biên trên |
| 30 | 27.51 | 17.5 | R04 | SAFE | Qua biên trên |
| 60 | 35 | 35 | R03 | WARNING | Tại `D_min` |
| 80.01 | 69.99 | 70 | R02 | DANGER | Vừa vượt mốc 80 km/h |
| 120.01 | 110 | — | — | ERROR | Từ chối tại Validation |

Các dữ liệu tham chiếu đầy đủ TC01–TC30 được lưu tại `tests/test_data/test_cases.csv`. Quy trình và tiêu chí kiểm thử thuộc `docs/test_documentation.md`; kết quả chạy thực tế thuộc `docs/test_results.md`.

## 9. Thứ tự thực thi và nguyên tắc bảo trì

```text
UI nhập speed, distance
         |
         v
Main: validate_input(speed, distance)
         |
    +----+----+
    |         |
 Không hợp lệ Hợp lệ
    |         |
  ERROR       v
          calculate_d_min(V)
               |
               v
         R01 -> R02 -> R03 -> R04
               |
               v
          Kết quả suy luận
               |
               v
        Main kiểm tra kết quả -> UI
```

Khi sửa tham số `MAX_SPEED`, `DELTA`, công thức `D_min`, thứ tự điều kiện hoặc nội dung `RULES`, nhóm cần đối chiếu đồng thời `src/rules.py`, `src/inference.py`, `src/validation.py`, `docs/test_documentation.md` và các bài test. Mỗi thay đổi logic phải có kiểm thử phù hợp trước khi merge.

**Giới hạn:** Phân loại `SAFE` chỉ là kết quả áp dụng các luật của bản mô phỏng trên hai biến đầu vào. Tài liệu này không tuyên bố đủ dữ liệu để xác nhận tình trạng an toàn hay va chạm ngoài thực tế.
