# ĐỀ TÀI: HỆ THỐNG CẢNH BÁO VA CHẠM 
## 1. Project Overview
Dự án phát triển dựa trên nền tảng AI Expert System, trong đó người dùng nhập input và hệ thống cung cấp cảnh báo dựa trên các mức độ rủi ro khác nhau. 

Hệ thống sử dụng cơ chế suy luận dựa trên luật (Rule-Based Reasoning), kết hợp cơ sở tri thức (Knowledge Base) và bộ suy luận (Inference Engine) để đánh giá điều kiện đầu vào, xác định mức độ rủi ro và đưa ra kết quả tương ứng. 

## 2. Mục tiêu dự án
- Xây dựng cơ sở tri thức chứa các luật chuyên môn
- Thiết kế và triển khai bộ suy luận để xử lý dữ liệu đầu vào
- Áp dụng các luật IF-THEN để phân loại mức độ rủi ro
- Đưa ra kết quả và thông báo cảnh báo tương ứng
- Xây dựng bộ dữ liệu kiểm thử nhằm đánh giá tính chính xác của hệ thống

## 3. Chức năng chính
- Tiếp nhận và kiểm tra tính hợp lệ của dữ liệu đầu vào
- Xây dựng và quản lý tập luật IF-THEN
- Thực hiện suy luận dựa trên các luật đã định nghĩa 
- Phân loại kết quả thành các mức độ:
    - SAFE: an toàn
    - WARNING: cảnh báo
    - DANGER: nguy hiểm 
    - ERROR: dữ liệu không hợp lệ hoặc vượt ngoài phạm vi xử lý
- Xuất kết quả phân loại và thông báo cảnh báo
- Kiểm thử hệ thống bằng dữ liệu mô phỏng 

## 4. Ngôn ngữ lập trình và các phương pháp sử dụng trong dự án
- Ngôn ngữ lập trình: Python 3.x
- Phương pháp xây dựng: Rule-Based System
- Biểu diễn các luật xây dựng: IF-THEN Rules

## 5. Cấu trúc dự án
```text
    AI-PROJECT/
    │
    ├── README.md
    ├── LICENSE
    ├── .gitignore
    ├── requirements.txt
    │
    ├── src/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── validation.py
    │   ├── rules.py
    │   ├── inference.py
    │   └── interface.py
    │
    ├── tests/
    │   ├── test_validation.py
    │   ├── test_inference.py
    │   ├── test_main.py
    │   └── test_data/
    │       └── test_cases.csv
    │
    └── docs/
        ├── module_contracts.md
        ├── rule_specification.md
        ├── test_documentation.md
        ├── test_results.md
        └── evidence/
            ├── evidence_01.png
            └── evidence_02.png
```

Các tài liệu chi tiết của dự án được trình bày tại:

## Tài liệu dự án

- [Module Contracts](docs/module_contracts.md): Đặc tả chức năng và trách nhiệm của các module.
- [Test Documentation](docs/test_documentation.md): Mô tả môi trường, phạm vi và các trường hợp kiểm thử.
- [Test Results](docs/test_results.md): Tổng hợp kết quả thực hiện kiểm thử.
- [Test Evidence](docs/evidence/): Thư mục chứa ảnh minh chứng quá trình kiểm thử.
- [Rule Specification](docs/rule_specification.md): Đặc tả cơ sở tri thức, các ngưỡng cảnh báo và tập luật R01–R04.

## 6. Quy trình làm việc nhóm 
- Làm việc theo nhánh riêng theo từng chức năng được phân công
- Cập nhật mã nguồn mới nhất từ nhánh phát triển trước khi bắt đầu công việc
- Đặt tên commit rõ ràng, thể hiện nội dung thay đổi 
- Không tự ý chỉnh sửa hoặc đẩy mã nguồn trực tiếp lên nhánh chính
- Tạo Pull Request để kiểm tra mã nguồn trước khi hợp nhất
- Thống nhất cấu trúc thư mục và quy ước lập trình toàn nhóm 


## 7. Hướng dẫn cài đặt và chạy chương trình

### 7.1. Yêu cầu môi trường

- Python 3.13 (khuyến nghị).
- Git.
- Tkinter (được hỗ trợ trong bản cài đặt Python).
- pytest (được khai báo trong `requirements.txt`).

### 7.2. Cài đặt dự án

Clone repository:

```bash
git clone https://github.com/minhthu1308/AI-PROJECT.git
cd AI-PROJECT
```

Cài đặt các thư viện cần thiết:

```bash
python -m pip install -r requirements.txt
```

### 7.3. Chạy chương trình

Từ thư mục gốc của dự án, chạy:

```bash
python -m src.main
```

Chương trình khởi chạy giao diện Tkinter, cho phép người dùng nhập tốc độ (km/h) và khoảng cách (m), sau đó hiển thị kết quả cảnh báo.

## 8. Hướng dẫn kiểm thử

### 8.1. Công cụ kiểm thử

Dự án sử dụng `pytest` để thực hiện kiểm thử tự động.

### 8.2. Chạy kiểm thử

Từ thư mục gốc của dự án, chạy:

```bash
python -m pytest tests/ -v -ra
```

### 8.3. Phạm vi kiểm thử

- `test_validation.py`: Kiểm tra tính hợp lệ của dữ liệu đầu vào.
- `test_inference.py`: Kiểm tra tính toán D_min và các luật R01–R04.
- `test_main.py`: Kiểm tra điều phối và tích hợp giữa Validation, Inference và Main.

Các trường hợp kiểm thử bao gồm:
- Dữ liệu hợp lệ.
- Dữ liệu không hợp lệ.
- Các giá trị biên.
- Trường hợp đặc biệt R01.
- Xử lý lỗi và kết quả không đúng cấu trúc.

Bộ dữ liệu kiểm thử được lưu trong `tests/test_data/test_cases.csv`.

Chi tiết xem tại [Tài liệu kiểm thử](docs/test_documentation.md).
