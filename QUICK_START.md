# 🚀 Hướng dẫn nhanh Auto Sora

Hướng dẫn sử dụng nhanh cho người dùng cuối.

## 📥 Download và Cài đặt

### Bước 1: Download
1. Download file `SoraAutomation.exe` 
2. Download `chromedriver.exe` tương thích với Chrome
3. Đặt cả 2 files trong cùng 1 thư mục

### Bước 2: Cài đặt Chrome
- Đảm bảo Google Chrome đã được cài đặt
- Phiên bản Chrome mới nhất được khuyến nghị

### Bước 3: Đăng nhập Sora
- Truy cập: https://sora.chatgpt.com/
- Đăng nhập tài khoản OpenAI
- Đảm bảo có quyền truy cập Sora

## 🎯 Sử dụng cơ bản

### Bước 1: Khởi động
1. **Double-click `SoraAutomation.exe`**
2. **Click "Launch Chrome"**
3. Chờ Chrome mở và tự động điều hướng đến Sora

### Bước 2: Chuẩn bị ảnh

**Cách 1: Tạo Excel từ folder ảnh (Đơn giản)**
1. Click **"Create Excel from Folder"**
2. Chọn folder chứa ảnh
3. Nhập prompt mặc định (ví dụ: "vẽ lại theo phong cách anime")
4. File Excel sẽ được tạo tự động

**Cách 2: Sử dụng Excel có sẵn (Nâng cao)**
1. Tạo file Excel với format:
   ```
   | Tên ảnh | Đường dẫn | Prompt | Trạng thái |
   | 001.png | C:\path\001.png | Prompt text | Pending |
   ```
2. Click **"Browse Excel"** và chọn file

### Bước 3: Bắt đầu xử lý
1. **Click "Start Upload"**
2. **Theo dõi log** để xem tiến trình
3. **Chờ hoàn thành** (mỗi ảnh ~3 phút)

## ⚙️ Cài đặt nhanh

### Delays mặc định (Khuyến nghị):
- **Sau Upload**: 10 giây
- **Sau Prompt**: 1 giây  
- **Trước Remix**: 1 giây
- **Sau Remix**: 180 giây (3 phút)

### Nếu muốn nhanh hơn:
- Giảm "Sau Remix" xuống 120 giây (2 phút)
- **Lưu ý**: Quá nhanh có thể làm ảnh chưa generate xong

### Nếu muốn chắc chắn hơn:
- Tăng "Sau Remix" lên 240 giây (4 phút)
- Tăng "Sau Upload" lên 15 giây

## 📊 Theo dõi tiến trình

### Log messages quan trọng:
```
[Ảnh 1] Bắt đầu xử lý...
[Ảnh 1] Đã upload ảnh
[Ảnh 1] Đã nhập prompt
[Ảnh 1] Đã click nút Remix
[Ảnh 1] Đang chờ 180 giây sau Remix...
[Ảnh 1] Hoàn thành! Còn 9 ảnh chưa xử lý
```

### Trạng thái trong Excel:
- **Pending**: Chưa xử lý
- **Completed**: Đã hoàn thành
- **Error**: Có lỗi xảy ra

## ❗ Lỗi thường gặp

### 1. Chrome không mở được
**Nguyên nhân**: Đường dẫn Chrome sai hoặc Chrome chưa cài
**Giải pháp**: 
- Cài đặt Chrome tại đường dẫn mặc định
- Hoặc chạy với quyền Administrator

### 2. ChromeDriver lỗi
**Nguyên nhân**: ChromeDriver không tương thích với Chrome
**Giải pháp**:
- Download ChromeDriver mới từ: https://chromedriver.chromium.org/
- Đảm bảo version ChromeDriver = version Chrome

### 3. Không tìm thấy nút Upload/Remix
**Nguyên nhân**: Sora đã thay đổi giao diện hoặc chưa đăng nhập
**Giải pháp**:
- Refresh trang Sora
- Đăng nhập lại
- Kiểm tra có ở đúng trang Sora không

### 4. Upload ảnh thất bại
**Nguyên nhân**: Đường dẫn ảnh sai hoặc file không tồn tại
**Giải pháp**:
- Kiểm tra đường dẫn trong Excel
- Đảm bảo file ảnh tồn tại
- Kiểm tra định dạng ảnh (PNG, JPG, JPEG, GIF, BMP)

### 5. Excel bị lỗi
**Nguyên nhân**: File Excel đang được mở bởi chương trình khác
**Giải pháp**:
- Đóng Excel trước khi chạy
- Kiểm tra quyền ghi file

## 💡 Tips sử dụng

### Để có kết quả tốt nhất:
1. **Sử dụng ảnh chất lượng cao** (ít nhất 512x512)
2. **Prompt rõ ràng và chi tiết**
3. **Không sử dụng máy cho việc khác** khi đang chạy
4. **Đảm bảo kết nối internet ổn định**

### Prompt hay dùng:
- "vẽ lại theo phong cách anime, giữ nguyên khuôn mặt nhân vật"
- "chuyển thành phong cách hoạt hình Disney"
- "tạo video ngắn với hiệu ứng chuyển động nhẹ"
- "thêm hiệu ứng ánh sáng và màu sắc sống động"

### Tối ưu hiệu suất:
- **Xử lý 10-20 ảnh mỗi lần** (tránh quá nhiều)
- **Chạy vào giờ ít người dùng** (tránh rate limit)
- **Backup dữ liệu** trước khi xử lý

## 🔄 Workflow khuyến nghị

### Cho người mới:
1. **Test với 2-3 ảnh** trước
2. **Sử dụng prompt đơn giản**
3. **Giữ delays mặc định**
4. **Theo dõi log cẩn thận**

### Cho người có kinh nghiệm:
1. **Batch xử lý 20-50 ảnh**
2. **Tùy chỉnh prompt cho từng ảnh**
3. **Điều chỉnh delays tối ưu**
4. **Sử dụng Excel nâng cao**

## 📞 Hỗ trợ

### Khi gặp vấn đề:
1. **Đọc log chi tiết** trong ứng dụng
2. **Kiểm tra trạng thái** trong file Excel
3. **Thử lại với 1 ảnh** để test
4. **Restart Chrome** nếu cần

### Thông tin hệ thống:
- **OS**: Windows 10/11
- **Chrome**: Version 120+
- **RAM**: Tối thiểu 4GB
- **Disk**: 1GB trống

---

**🎉 Chúc bạn sử dụng thành công Auto Sora!**

Mỗi ảnh sẽ mất khoảng 3 phút để xử lý. Hãy kiên nhẫn và theo dõi log để đảm bảo mọi thứ hoạt động tốt.
