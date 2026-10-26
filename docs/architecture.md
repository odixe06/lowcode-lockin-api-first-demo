# Thiết kế và checklist

API có `GET /tickets`, `POST /tickets`, `GET /export`, `GET /health`, `GET /openapi.json`. ID do backend cấp, title được trim và phải dài 1 đến 120 ký tự. `status=open` là quy tắc cố định của demo.

UI A không truy cập SQLite. Node-RED proxy request đến địa chỉ `API_URL`. UI B dùng API cùng origin. Không cần nới CORS. Dữ liệu người dùng được hiển thị bằng `textContent`, không ghép HTML.

Kiểm tra trước buổi trình bày: 8000 và 1880 chưa bị ứng dụng khác dùng, pull image trước, mở sẵn hai UI, dùng dữ liệu giả. Ghi ID trước khi dừng UI A. Muốn chạy lại UI A: `docker compose start ui_a`.

Nếu lỗi kết nối UI A: xem `docker compose logs ui_a api`, xác nhận API_URL là `http://api:8000` trong Docker hoặc `http://127.0.0.1:8000` khi chạy npm. Container truy cập localhost của chính nó, không phải host.

Tiêu chí thành công: ID không đổi, nội dung không mất, API tiếp tục validation, UI B tạo được bản ghi mới. Migration sang database khác và chuyển workflow nằm ngoài phạm vi demo này.
