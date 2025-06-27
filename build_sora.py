import PyInstaller.__main__
import os
import shutil
import sys

def build_sora():
    PROJECT_NAME = "SoraAutomation"
    ENTRY_FILE = "main.py"
    ICON_FILE = "icon.ico" if os.path.exists("icon.ico") else None

    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(current_dir, "build")
    dist_dir = os.path.join(current_dir, "dist")
    spec_dir = current_dir

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        print(f"Đã xóa thư mục build cũ: {build_dir}")

    build_cmd = [
        ENTRY_FILE,
        f'--name={PROJECT_NAME}',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        f'--distpath={dist_dir}',
        f'--workpath={build_dir}',
        f'--specpath={spec_dir}'
    ]

    if ICON_FILE:
        build_cmd.append(f'--icon={ICON_FILE}')

    print('🛠️ Đang build file .exe...')
    try:
        PyInstaller.__main__.run(build_cmd)
        print('✅ Build thành công!')
    except Exception as e:
        print(f'❌ Lỗi khi build: {str(e)}')
        sys.exit(1)

    print(f'\n📁 File .exe đã được tạo tại: {dist_dir}')
    print(f'📋 Khi chạy, cần đặt chromedriver.exe cùng thư mục với file .exe (không cần chrome-automation)')

if __name__ == '__main__':
    build_sora()