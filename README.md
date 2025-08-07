# Auto Sora - Tự động hóa Sora AI

Chương trình tự động upload ảnh và tạo video với Sora AI của OpenAI.

## 📋 Mục lục
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Cách chạy](#cách-chạy)
- [Build file EXE](#build-file-exe)
- [Cấu hình](#cấu-hình)
- [Sử dụng](#sử-dụng)
- [Troubleshooting](#troubleshooting)

## 🖥️ Yêu cầu hệ thống

### Phần mềm bắt buộc:
- **Windows 10/11**
- **Python 3.8+** (nếu chạy từ source code)
- **Google Chrome** (phiên bản mới nhất)
- **ChromeDriver** (tương thích với Chrome)

### Tài khoản:
- **Tài khoản OpenAI** có quyền truy cập Sora
- **Đã đăng nhập Sora** tại: https://sora.chatgpt.com/

## 📦 Cài đặt

### Cách 1: Chạy từ Source Code

1. **Clone hoặc download project**
```bash
git clone <repository-url>
cd auto-sora
```

2. **Cài đặt Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Download ChromeDriver**
   - Truy cập: https://chromedriver.chromium.org/
   - Download phiên bản tương thích với Chrome
   - Giải nén và đặt `chromedriver.exe` vào thư mục project

4. **Cập nhật đường dẫn** (nếu cần)
   - Mở `main.py`
   - Sửa `CHROME_PATH` và `CHROMEDRIVER_PATH` nếu khác mặc định

### Cách 2: Sử dụng File EXE

1. **Download file EXE** từ releases
2. **Đặt `chromedriver.exe`** cùng thư mục với file EXE
3. **Đảm bảo Chrome đã cài đặt** tại đường dẫn mặc định

## 🚀 Cách chạy

### Chạy từ Source Code:
```bash
python main.py
```

### Chạy từ File EXE:
```bash
SoraAutomation.exe
```

## 🔨 Build file EXE

### Yêu cầu:
```bash
pip install pyinstaller
```

### Build:
```bash
python build_sora.py
```

File EXE sẽ được tạo trong thư mục `dist/`

### Cấu trúc sau khi build:
```
dist/
├── SoraAutomation.exe
└── chrome-automation/ (Chrome profile data)
```

## ⚙️ Cấu hình

### Đường dẫn mặc định:
- **Chrome**: `C:\Program Files\Google\Chrome\Application\chrome.exe`
- **ChromeDriver**: `chromedriver.exe` (cùng thư mục)
- **Sora URL**: `https://sora.chatgpt.com/explore`

### Delays mặc định:
- **Sau Upload**: 10 giây
- **Sau Prompt**: 1 giây
- **Trước Remix**: 1 giây
- **Sau Remix**: 180 giây (3 phút)

### Cấu hình Excel:
- **Cột A**: Tên ảnh
- **Cột B**: Đường dẫn ảnh
- **Cột C**: Prompt
- **Cột D**: Trạng thái

## 📖 Sử dụng

### Bước 1: Khởi động Chrome
1. Click **"Launch Chrome"**
2. Đăng nhập Sora nếu chưa
3. Đảm bảo ở trang Sora

### Bước 2: Chuẩn bị dữ liệu
**Cách 1: Sử dụng Excel**
1. Tạo file Excel với format:
   ```
   | Tên ảnh | Đường dẫn | Prompt | Trạng thái |
   | 001.png | C:\path\001.png | Prompt text | Pending |
   ```
2. Click **"Browse Excel"** và chọn file

**Cách 2: Tạo từ folder**
1. Click **"Create Excel from Folder"**
2. Chọn folder chứa ảnh
3. Nhập prompt mặc định

### Bước 3: Cấu hình Delays
- Điều chỉnh các thời gian chờ nếu cần
- **Sau Remix** là thời gian chờ chính (3 phút)

### Bước 4: Bắt đầu xử lý
1. Click **"Start Upload"**
2. Theo dõi log để xem tiến trình
3. Click **"Stop"** để dừng nếu cần

### Flow xử lý:
```
Upload ảnh → Chờ 10s → Nhập prompt → Chờ 1s → 
Chờ 1s → Click Remix → Chờ 180s → Ảnh tiếp theo
```

## 🔧 Troubleshooting

### Lỗi thường gặp:

**1. Chrome không khởi động được**
- Kiểm tra đường dẫn Chrome
- Đảm bảo Chrome đã cài đặt
- Thử chạy với quyền Administrator

**2. ChromeDriver lỗi**
- Kiểm tra phiên bản ChromeDriver vs Chrome
- Download ChromeDriver mới từ trang chính thức
- Đặt đúng đường dẫn

**3. Không tìm thấy elements**
- Sora có thể đã thay đổi giao diện
- Thử refresh trang Sora
- Kiểm tra đã đăng nhập chưa

**4. Upload ảnh thất bại**
- Kiểm tra đường dẫn ảnh có đúng không
- Đảm bảo file ảnh tồn tại
- Kiểm tra định dạng ảnh (PNG, JPG, JPEG, GIF, BMP)

**5. Excel lỗi**
- Đóng file Excel trước khi chạy
- Kiểm tra format Excel đúng
- Đảm bảo có quyền ghi file

### Debug:
- Xem log trong giao diện
- Kiểm tra file Excel để xem trạng thái
- Chụp screenshot khi có lỗi

## 📝 Ghi chú

### Giới hạn:
- Sora có thể có rate limit
- Chỉ hỗ trợ Windows
- Cần kết nối internet ổn định

### Bảo mật:
- Không lưu trữ thông tin đăng nhập
- Sử dụng Chrome profile riêng
- Dữ liệu chỉ lưu local

### Performance:
- Mỗi ảnh mất khoảng 3.2 phút
- Có thể điều chỉnh delays để tối ưu
- RAM sử dụng: ~200-500MB

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra [Troubleshooting](#troubleshooting)
2. Xem log chi tiết trong ứng dụng
3. Đảm bảo đã follow đúng hướng dẫn

---

**Phiên bản**: 1.0  
**Cập nhật**: 2025-01-08  
**Tương thích**: Windows 10/11, Chrome 120+
