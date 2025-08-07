# 🔨 Hướng dẫn Build Auto Sora

Hướng dẫn chi tiết để build file executable (.exe) từ source code.

## 📋 Yêu cầu Build

### Phần mềm:
- **Python 3.8+**
- **pip** (Python package manager)
- **Git** (optional, để clone repo)

### Dependencies:
```bash
pip install pyinstaller
pip install -r requirements.txt
```

## 🚀 Các bước Build

### Bước 1: Chuẩn bị môi trường

1. **Clone/Download source code**
```bash
git clone <repository-url>
cd auto-sora
```

2. **Tạo virtual environment** (khuyến nghị)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Bước 2: Kiểm tra trước khi build

1. **Test chạy source code**
```bash
python main.py
```

2. **Đảm bảo tất cả imports hoạt động**
3. **Kiểm tra đường dẫn Chrome và ChromeDriver**

### Bước 3: Build executable

**Cách 1: Sử dụng script build có sẵn**
```bash
python build_sora.py
```

**Cách 2: Build thủ công**
```bash
pyinstaller --onefile --windowed --name="SoraAutomation" --icon=icon.ico main.py
```

### Bước 4: Kiểm tra kết quả

1. **Kiểm tra thư mục `dist/`**
```
dist/
├── SoraAutomation.exe
└── chrome-automation/ (nếu có)
```

2. **Test file exe**
```bash
cd dist
SoraAutomation.exe
```

## ⚙️ Tùy chỉnh Build

### File `build_sora.py` có các tùy chọn:

```python
# Tên file output
name = "SoraAutomation"

# Icon (nếu có)
icon = "icon.ico"

# Ẩn console window
windowed = True

# Đóng gói thành 1 file
onefile = True

# Thêm data files
datas = [
    ('requirements.txt', '.'),
    # Thêm files khác nếu cần
]

# Ẩn imports
hiddenimports = [
    'selenium',
    'pandas',
    'openpyxl',
    'tkinter'
]
```

### Các tùy chọn PyInstaller:

```bash
# Build thành 1 file duy nhất
--onefile

# Ẩn console window
--windowed

# Thêm icon
--icon=icon.ico

# Tên file output
--name="SoraAutomation"

# Thêm data files
--add-data="file.txt;."

# Ẩn imports
--hidden-import=module_name

# Exclude modules
--exclude-module=module_name
```

## 📁 Cấu trúc Project

### Trước khi build:
```
auto-sora/
├── main.py                 # File chính
├── build_sora.py          # Script build
├── requirements.txt       # Dependencies
├── README.md             # Hướng dẫn
├── BUILD_GUIDE.md        # Hướng dẫn build
├── icon.ico              # Icon (optional)
├── chromedriver.exe      # ChromeDriver
└── chrome-automation/    # Chrome profile
```

### Sau khi build:
```
auto-sora/
├── ... (files gốc)
├── build/                # Temp build files
├── dist/                 # Output folder
│   ├── SoraAutomation.exe
│   └── chrome-automation/
└── SoraAutomation.spec   # PyInstaller spec file
```

## 🔧 Troubleshooting Build

### Lỗi thường gặp:

**1. ModuleNotFoundError**
```bash
# Thêm hidden import
--hidden-import=module_name

# Hoặc cài đặt module thiếu
pip install module_name
```

**2. File không tìm thấy**
```bash
# Thêm data files
--add-data="file.txt;."
```

**3. Build quá lâu**
```bash
# Exclude modules không cần thiết
--exclude-module=matplotlib
--exclude-module=numpy
```

**4. File exe quá lớn**
```bash
# Sử dụng --onedir thay vì --onefile
# Exclude modules không cần thiết
# Sử dụng UPX để nén (optional)
```

**5. Antivirus chặn**
- Thêm exception cho thư mục build
- Sử dụng certificate để sign file exe
- Build trên máy sạch

### Debug build:

**1. Xem log chi tiết**
```bash
pyinstaller --log-level=DEBUG main.py
```

**2. Kiểm tra dependencies**
```bash
pipdeptree
```

**3. Test imports**
```python
import sys
print(sys.path)
import module_name  # Test từng module
```

## 📦 Tối ưu Build

### Giảm kích thước file:

1. **Exclude modules không cần**
```python
excludes = [
    'matplotlib',
    'numpy',
    'scipy',
    'PIL',
    'cv2'
]
```

2. **Sử dụng --onedir**
```bash
pyinstaller --onedir main.py
```

3. **Nén với UPX**
```bash
# Download UPX
# Thêm --upx-dir=path/to/upx
pyinstaller --upx-dir=upx main.py
```

### Tăng tốc độ khởi động:

1. **Lazy imports**
```python
# Import trong function thay vì top level
def function():
    import heavy_module
```

2. **Optimize imports**
```python
# Chỉ import những gì cần
from module import specific_function
```

## 🚀 Deploy

### Chuẩn bị package:

1. **Tạo thư mục deploy**
```
SoraAutomation/
├── SoraAutomation.exe
├── chromedriver.exe
├── README.md
└── chrome-automation/ (optional)
```

2. **Tạo installer** (optional)
- Sử dụng NSIS
- Hoặc Inno Setup
- Hoặc WiX Toolset

3. **Test trên máy khác**
- Máy không có Python
- Máy không có dependencies
- Các phiên bản Windows khác nhau

## 📝 Checklist Build

### Trước khi build:
- [ ] Code chạy OK từ source
- [ ] Tất cả dependencies đã cài
- [ ] Đường dẫn files đã đúng
- [ ] Icon đã chuẩn bị (nếu có)

### Sau khi build:
- [ ] File exe tạo thành công
- [ ] Kích thước file hợp lý
- [ ] Test chạy file exe
- [ ] Test trên máy khác
- [ ] Antivirus không chặn

### Trước khi release:
- [ ] Version number đã update
- [ ] README đã update
- [ ] Test đầy đủ tính năng
- [ ] Tạo backup source code

---

**Lưu ý**: Build có thể mất 5-15 phút tùy vào cấu hình máy và số lượng dependencies.
