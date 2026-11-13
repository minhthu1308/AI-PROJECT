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
- Thực hiện suy luận dựa trên các luật đã định nghãi
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

## 6. Quy trình làm việc nhóm 
- Làm việc theo nhánh riêng theo từng chức năng được phân công
- Cập nhật mã nguồn mới nhất từ nhánh phát triển trước khi bắt đầu công việc
- Đặt tên commit rõ ràng, thể hiện nội dung thay đổi 
- Không tự ý chỉnh sửa hoặc đẩy mã nguồn trực tiếp lên nhánh chính
- Tạo Pull Request để kiểm tra mã nguồn trước khi hợp nhất
- Thống nhất cấu trúc thư mục và quy ước lập trình toàn nhóm 

