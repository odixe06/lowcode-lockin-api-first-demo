# Báo cáo kiểm thử

Kiểm tra ngày 26/10/2026. Môi trường: Linux, Python 3.12.14, Node.js 24.22.1, Node-RED 4.1.0 cài bằng npm. Không có Docker trong môi trường kiểm thử.

## Đã chạy và đạt

* Hai test Python kiểm tra validation, Unicode, ID và dữ liệu sau API restart, JSON export và OpenAPI.
* Node-RED thật trả HTTP 200 cho UI A.
* Tạo bản ghi qua proxy Node-RED trả HTTP 201. API độc lập đọc đúng ID và nội dung.
* Title toàn dấu cách qua Node-RED trả HTTP 400.
* Dừng process Node-RED, API vẫn giữ bản ghi và tạo bản ghi mới với HTTP 201.

## Chưa kiểm tra

Docker image, lệnh Docker Compose trên máy đích và thao tác click qua mọi trình duyệt chưa được chạy tại đây. Kiểm thử HTTP không thay cho kiểm thử giao diện đầy đủ. Chưa kiểm tra bảo mật hoặc tải production. Không có số đo benchmark hay chi phí migration doanh nghiệp.
