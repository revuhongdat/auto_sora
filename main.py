# -*- coding: utf-8 -*-
import os
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# --- Các thư viện của bên thứ ba ---
# Cần cài đặt bằng pip: pip install selenium pandas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ===================== HẰNG SỐ CẤU HÌNH =====================
CHROME_PATH = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
CHROMEDRIVER_PATH = r"C:\\Users\\Admin\\Desktop\\auto sora\\137\\chromedriver-win64\\chromedriver.exe"
SORA_URL = "https://sora.chatgpt.com/library"
SELECTORS = {
    "add_button": "//button[.//span[text()='Attach media']]",
    "add_button_alternatives": [
        "//button[contains(@aria-label, 'Attach')]",
        "//button[contains(@title, 'Attach')]",
        "//button[.//svg[contains(@class, 'paperclip')]]",
        "//button[@data-testid='attach-button']"
    ],
    "upload_button": "//div[normalize-space()='Upload from device']",
    "prompt_input": "(//textarea[@placeholder='Describe a new image...'])[1]",
    "prompt_input_alternatives": [
        "//textarea[contains(@placeholder, 'Describe')]",
        "//textarea[contains(@placeholder, 'image')]",
        "//input[contains(@placeholder, 'Describe')]",
        "//div[contains(@contenteditable, 'true')]"
    ],
    "remix_button": "(//button[normalize-space()='Remix'])[1]",
    "remix_button_alternatives": [
        "//button[contains(text(), 'Remix')]",
        "//button[contains(@class, 'remix')]",
        "//button[@data-testid='remix-button']",
        "//button[.//span[contains(text(), 'Remix')]]"
    ],
    "upload_input": "//input[@type='file']",
    # Selectors để kiểm tra trạng thái generation
    "generation_list": "//div[@role='dialog']//a[contains(@href, '/t/') or contains(@href, '/g/')]",
    "loading_spinner": ".//svg[contains(@class, 'h-6 w-6')]//circle[@stroke-dasharray]",
    "generation_thumbnail": ".//img[@alt='Sora generation']",
    "generation_cancelled": ".//svg[contains(@class, 'lucide-ban')]",
    "generation_progress": ".//div[contains(text(), '%')]",
    # Selectors mới cho preview area
    "preview_area": "//div[contains(@style, 'aspect-ratio')]",
    "preview_loading": "//div[contains(@style, 'aspect-ratio')]//svg[@viewBox='0 0 120 120']",
    "preview_progress": "//div[contains(@style, 'aspect-ratio')]//div[contains(text(), '%')]",
    "preview_completed": "//div[contains(@style, 'aspect-ratio')]//img",
    "main_generation_area": "//div[contains(@class, 'bg-token-bg-secondary')]//svg[@width='120'][@height='120']",
    "main_progress_text": "//div[contains(@class, 'absolute')]//div[contains(text(), '%')]"
}
DELAYS = {
    "after_click": 2.0,
    "after_upload": 10.0,
    "after_prompt": 1.0,
    "before_remix": 1.0,
    "after_remix": 180.0  # 3 phút chờ sau remix, sau đó tiếp tục ảnh tiếp theo luôn
}
IMAGE_FOLDER = r"C:/Users/Admin/Desktop/auto sora/test"
PROMPT = "vẽ lại theo phong cách anime, giữ nguyên khuôn mặt nhân vật, thay đổi backgound cho hợp lý"
EXCEL_FILENAME = "image_list.xlsx"
EXCEL_COLUMNS = {
    "name": "Image Name",
    "path": "Image Path",
    "prompt": "Prompt",
    "status": "Status"
}
HEADLESS = False
# ============================================================

# ==============================================================================
# PHẦN 1: LOGIC CỐT LÕI (GIỮ NGUYÊN)
# ==============================================================================

class ChromeProfileAutomation:
    def __init__(self, chrome_path, chrome_driver_path):
        self.chrome_path = chrome_path
        self.chrome_driver_path = chrome_driver_path
        self.driver = None
        self.chrome_process = None
        self.debug_port = None

        if not os.path.exists(self.chrome_path):
            raise Exception(f"Không tìm thấy Chrome tại: {self.chrome_path}")
        if self.chrome_driver_path and not os.path.exists(self.chrome_driver_path):
            raise Exception(f"Không tìm thấy ChromeDriver tại: {self.chrome_driver_path}")

    def launch_chrome_with_profile(self, url=SORA_URL, headless=HEADLESS):
        try:
            chrome_options = Options()
            chrome_options.binary_location = self.chrome_path
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)

            if headless:
                chrome_options.add_argument("--headless=new")

            automation_dir = os.path.join(os.getcwd(), "chrome-automation")
            if not os.path.exists(automation_dir):
                os.makedirs(automation_dir)
            chrome_options.add_argument(f"--user-data-dir={automation_dir}")

            service = Service(self.chrome_driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.get(url)
            time.sleep(2)
            return True, "Chrome đã mở và kết nối Selenium thành công (sử dụng profile tự động)."

        except Exception as e:
            return False, f"Lỗi khi khởi động Chrome: {str(e)}"

    def get_current_url(self):
        if self.driver:
            return self.driver.current_url
        return None

    def get_page_title(self):
        if self.driver:
            return self.driver.title
        return None

    def close_chrome(self):
        try:
            if self.driver:
                self.driver.quit()
            if self.chrome_process:
                self.chrome_process.terminate()
            return True, "Đã đóng Chrome thành công"
        except Exception as e:
            return False, f"Lỗi khi đóng: {str(e)}"


class SoraAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.is_running = False
        self.selectors = SELECTORS
        self.delays = DELAYS
        self.excel_cols = EXCEL_COLUMNS
        self.ui = None

    def set_ui(self, ui):
        self.ui = ui

    def _log(self, message):
        if self.ui:
            self.ui.root.after(0, self.ui.log_message, message)
        else:
            print(f"[{time.strftime('%H:%M:%S')}] {message}")

    def _check_page_state(self):
        """Kiểm tra trạng thái trang hiện tại để debug"""
        try:
            current_url = self.driver.current_url
            page_title = self.driver.title
            return f"URL: {current_url}, Title: {page_title}"
        except Exception as e:
            return f"Không thể lấy thông tin trang: {e}"

    def _find_add_button_with_fallback(self, wait):
        """Tìm nút Add/Attach với các selector backup"""
        # Thử selector chính
        add_button_xpath = self.selectors["add_button"]
        try:
            add_button = wait.until(EC.element_to_be_clickable((By.XPATH, add_button_xpath)))
            return add_button, add_button_xpath
        except Exception:
            pass

        # Thử các selector backup
        for alt_selector in self.selectors.get("add_button_alternatives", []):
            try:
                add_button = wait.until(EC.element_to_be_clickable((By.XPATH, alt_selector)))
                return add_button, alt_selector
            except Exception:
                continue

        return None, None

    def _find_prompt_input_with_fallback(self, wait):
        """Tìm prompt input với các selector backup"""
        # Thử selector chính
        prompt_input_xpath = self.selectors["prompt_input"]
        try:
            prompt_input = wait.until(EC.visibility_of_element_located((By.XPATH, prompt_input_xpath)))
            return prompt_input, prompt_input_xpath
        except Exception:
            pass

        # Thử các selector backup
        for alt_selector in self.selectors.get("prompt_input_alternatives", []):
            try:
                prompt_input = wait.until(EC.visibility_of_element_located((By.XPATH, alt_selector)))
                return prompt_input, alt_selector
            except Exception:
                continue

        return None, None

    def _find_remix_button_with_fallback(self, wait):
        """Tìm nút Remix với các selector backup"""
        remix_button = None
        used_selector = None

        # Thử selector chính
        remix_button_xpath = self.selectors["remix_button"]
        try:
            remix_button = wait.until(EC.element_to_be_clickable((By.XPATH, remix_button_xpath)))
            used_selector = remix_button_xpath
            return remix_button, used_selector
        except Exception:
            pass

        # Thử các selector backup
        for alt_selector in self.selectors.get("remix_button_alternatives", []):
            try:
                remix_button = wait.until(EC.element_to_be_clickable((By.XPATH, alt_selector)))
                used_selector = alt_selector
                return remix_button, used_selector
            except Exception:
                continue

        return None, None

    def _safe_click(self, element, element_name="element"):
        """Click element một cách an toàn, thử nhiều phương pháp"""
        try:
            # Phương pháp 1: Click bình thường
            element.click()
            return True, "Click thành công"
        except Exception as e1:
            try:
                # Phương pháp 2: Scroll đến element rồi click
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                element.click()
                return True, "Click thành công sau scroll"
            except Exception as e2:
                try:
                    # Phương pháp 3: JavaScript click
                    self.driver.execute_script("arguments[0].click();", element)
                    return True, "Click thành công bằng JavaScript"
                except Exception as e3:
                    return False, f"Không thể click {element_name}: {e1}, {e2}, {e3}"

    def _safe_excel_save(self, df, excel_path, max_retries=3):
        """Lưu Excel file một cách an toàn với retry"""
        for attempt in range(max_retries):
            try:
                df.to_excel(excel_path, index=False)
                return True, "Lưu Excel thành công"
            except PermissionError:
                if attempt < max_retries - 1:
                    self._log(f"File Excel đang được sử dụng, thử lại sau 2 giây... (lần {attempt + 1})")
                    time.sleep(2)
                else:
                    return False, "Không thể lưu Excel - file đang được mở bởi chương trình khác"
            except Exception as e:
                return False, f"Lỗi khi lưu Excel: {e}"

        return False, "Đã thử tối đa số lần cho phép"

    def _check_generation_status(self):
        """Kiểm tra trạng thái generation của ảnh mới nhất"""
        try:
            # Phương pháp 1: Kiểm tra preview area chính (nơi hiển thị progress)
            preview_areas = self.driver.find_elements(By.XPATH, self.selectors["preview_area"])
            if preview_areas:
                for preview in preview_areas:
                    # Kiểm tra loading spinner trong preview
                    loading_spinners = preview.find_elements(By.XPATH, ".//svg[@viewBox='0 0 120 120']")
                    if loading_spinners:
                        # Tìm progress text
                        progress_elements = preview.find_elements(By.XPATH, ".//div[contains(text(), '%')]")
                        if progress_elements:
                            progress_text = progress_elements[0].text
                            return "generating", f"Đang generate: {progress_text}"
                        return "generating", "Đang generate..."

                    # Kiểm tra xem có ảnh hoàn thành không
                    completed_images = preview.find_elements(By.XPATH, ".//img")
                    if completed_images:
                        return "completed", "Generation đã hoàn thành"

            # Phương pháp 2: Kiểm tra main generation area
            main_spinners = self.driver.find_elements(By.XPATH, self.selectors["main_generation_area"])
            if main_spinners:
                # Tìm progress text
                progress_elements = self.driver.find_elements(By.XPATH, self.selectors["main_progress_text"])
                if progress_elements:
                    progress_text = progress_elements[0].text
                    return "generating", f"Đang generate: {progress_text}"
                return "generating", "Đang generate..."

            # Phương pháp 3: Kiểm tra danh sách generation (fallback)
            generation_items = self.driver.find_elements(By.XPATH, self.selectors["generation_list"])

            if generation_items:
                # Kiểm tra item đầu tiên (mới nhất)
                latest_item = generation_items[0]

                # Kiểm tra xem có loading spinner không
                loading_spinners = latest_item.find_elements(By.XPATH, self.selectors["loading_spinner"])
                if loading_spinners:
                    # Tìm progress text
                    progress_elements = latest_item.find_elements(By.XPATH, self.selectors["generation_progress"])
                    if progress_elements:
                        progress_text = progress_elements[0].text
                        return "generating", f"Đang generate: {progress_text}"
                    return "generating", "Đang generate..."

                # Kiểm tra xem có bị cancelled không
                cancelled_icons = latest_item.find_elements(By.XPATH, self.selectors["generation_cancelled"])
                if cancelled_icons:
                    return "cancelled", "Generation bị hủy"

                # Kiểm tra xem có thumbnail không (đã hoàn thành)
                thumbnails = latest_item.find_elements(By.XPATH, self.selectors["generation_thumbnail"])
                if thumbnails:
                    return "completed", "Generation đã hoàn thành"

            return "no_generations", "Không tìm thấy generation nào"

        except Exception as e:
            return "error", f"Lỗi khi kiểm tra trạng thái: {e}"

    def _wait_for_generation_complete(self, image_idx, timeout=1800):  # 30 phút timeout
        """Chờ cho generation hoàn thành"""
        self._log(f"[Ảnh {image_idx}] Bắt đầu chờ generation hoàn thành...")

        start_time = time.time()
        check_interval = 15  # Kiểm tra mỗi 15 giây
        last_status = None

        while time.time() - start_time < timeout:
            if not self.is_running:
                self._log(f"[Ảnh {image_idx}] Đã dừng xử lý trong khi chờ generation.")
                return False, "Đã dừng xử lý"

            # Kiểm tra cả generation status và preview area
            status, message = self._check_generation_status()
            preview_status, preview_message = self._check_preview_area_status()

            # Ưu tiên preview status nếu có thông tin
            if preview_status in ["generating", "completed"]:
                status, message = preview_status, preview_message

            # Chỉ log khi status thay đổi
            if status != last_status:
                elapsed = int(time.time() - start_time)
                self._log(f"[Ảnh {image_idx}] Trạng thái generation: {message} (đã chờ {elapsed}s)")
                if preview_status != "no_preview":
                    self._log(f"[Ảnh {image_idx}] Preview status: {preview_message}")
                last_status = status

            if status == "completed":
                self._log(f"[Ảnh {image_idx}] Generation đã hoàn thành!")
                return True, "Generation hoàn thành"
            elif status == "cancelled":
                self._log(f"[Ảnh {image_idx}] Generation bị hủy!")
                return False, "Generation bị hủy"
            elif status == "error":
                self._log(f"[Ảnh {image_idx}] Lỗi khi kiểm tra generation: {message}")
                # Tiếp tục thử lại

            time.sleep(check_interval)

        # Timeout
        elapsed = int(time.time() - start_time)
        self._log(f"[Ảnh {image_idx}] Timeout sau {elapsed}s khi chờ generation.")
        return False, f"Timeout sau {elapsed}s"

    def _check_preview_area_status(self):
        """Kiểm tra trạng thái preview area cụ thể"""
        try:
            # Tìm tất cả preview areas
            preview_selectors = [
                "//div[contains(@style, 'aspect-ratio: 720 / 480')]",
                "//div[contains(@style, 'aspect-ratio')]",
                "//a[contains(@class, 'group/tile')]//div[contains(@class, 'bg-token-bg-secondary')]"
            ]

            for selector in preview_selectors:
                previews = self.driver.find_elements(By.XPATH, selector)
                for preview in previews:
                    # Kiểm tra loading spinner
                    spinners = preview.find_elements(By.XPATH, ".//svg[@width='120'][@height='120']")
                    if spinners:
                        # Tìm progress text
                        progress_divs = preview.find_elements(By.XPATH, ".//div[contains(@class, 'absolute')]//div[contains(text(), '%')]")
                        if progress_divs:
                            progress = progress_divs[0].text.strip()
                            return "generating", f"Preview đang generate: {progress}"

                        # Kiểm tra circle progress
                        circles = preview.find_elements(By.XPATH, ".//circle[@stroke-dasharray]")
                        if circles:
                            return "generating", "Preview đang generate (có circle progress)"

                    # Kiểm tra ảnh hoàn thành
                    images = preview.find_elements(By.XPATH, ".//img")
                    if images:
                        return "completed", "Preview đã có ảnh hoàn thành"

            return "no_preview", "Không tìm thấy preview area"

        except Exception as e:
            return "error", f"Lỗi khi kiểm tra preview: {e}"

    def create_excel_from_folder(self, folder_path, excel_path, prompt_text):
        if os.path.exists(excel_path):
            return False, "File excel đã tồn tại"
        try:
            import pandas as pd
            image_files = []
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    name = os.path.splitext(file)[0]
                    path = os.path.normpath(os.path.abspath(os.path.join(folder_path, file)))
                    image_files.append({
                        self.excel_cols["name"]: name,
                        self.excel_cols["path"]: path,
                        self.excel_cols["prompt"]: prompt_text,
                        self.excel_cols["status"]: ''
                    })
            df = pd.DataFrame(image_files)
            df.to_excel(excel_path, index=False)
            return True, f"Đã tạo file excel với {len(image_files)} ảnh."
        except Exception as e:
            return False, f"Lỗi khi tạo file excel: {str(e)}"

    def process_images(self, excel_path):
        self.is_running = True
        try:
            import pandas as pd
            df = pd.read_excel(excel_path)
            # Lấy những ảnh có trạng thái khác "Completed"
            pending_images = df[
                df[self.excel_cols["status"]].isna() |
                (df[self.excel_cols["status"]] == '') |
                (df[self.excel_cols["status"]] != 'Completed')
            ].to_dict('records')

            # Thống kê trạng thái
            total_images = len(df)
            completed_images = len(df[df[self.excel_cols["status"]] == 'Completed'])
            pending_count = len(pending_images)

            self._log(f"Tổng số ảnh: {total_images}")
            self._log(f"Đã hoàn thành: {completed_images}")
            self._log(f"Cần xử lý: {pending_count}")

            if not pending_images:
                self._log("Tất cả ảnh đã được xử lý hoàn thành!")
                return True, "Tất cả ảnh đã được xử lý hoàn thành"

            self._log(f"Bắt đầu xử lý {pending_count} ảnh chưa hoàn thành...")

            wait = WebDriverWait(self.driver, 20)

            for idx, image in enumerate(pending_images):
                if not self.is_running:
                    self._log("Đã dừng xử lý")
                    return False, "Đã dừng xử lý"

                try:
                    # Hiển thị thông tin ảnh và trạng thái hiện tại
                    image_name = image[self.excel_cols['name']]
                    current_status = image.get(self.excel_cols["status"], "")
                    self._log(f"[{image_name}] Bắt đầu xử lý ({idx+1}/{pending_count}) - Trạng thái hiện tại: '{current_status}'")

                    # 1. Tìm và click add_button
                    self._log(f"[{image_name}] Đang tìm add button...")
                    add_button, add_button_xpath = self._find_add_button_with_fallback(wait)

                    if not add_button:
                        self._log(f"[{image_name}] Không tìm thấy add button với bất kỳ selector nào. Bỏ qua ảnh này.")
                        continue

                    self._log(f"[{image_name}] Đã tìm thấy add button với selector: {add_button_xpath}")
                    click_success, click_message = self._safe_click(add_button, "add button")

                    if not click_success:
                        self._log(f"[{image_name}] {click_message}")
                        continue

                    self._log(f"[{image_name}] {click_message}")
                    time.sleep(self.delays.get("after_click", 1))

                    # 2. Tìm upload input và upload ảnh (KHÔNG click upload_button)
                    upload_input_xpath = "//input[@accept='image/jpeg,image/png,image/webp']"
                    self._log(f"[{image_name}] Đang tìm upload input với selector: {upload_input_xpath}")
                    try:
                        file_input = wait.until(EC.presence_of_element_located((By.XPATH, upload_input_xpath)))
                        self._log(f"[{image_name}] Đã tìm thấy upload input.")
                        # Nếu input bị ẩn, thử hiện nó lên
                        self.driver.execute_script("arguments[0].style.display = 'block';", file_input)
                    except Exception as e:
                        self._log(f"[{image_name}] Không tìm thấy upload input với selector: {upload_input_xpath}. Lỗi: {e}")
                        continue

                    self._log(f"[{image_name}] Đang upload ảnh: {image[self.excel_cols['path']]}")
                    file_input.send_keys(image[self.excel_cols['path']])
                    time.sleep(self.delays.get("after_upload", 2))

                    # 4. Nhập prompt cho ảnh ngay sau khi upload
                    self._log(f"[{image_name}] Đang tìm prompt input...")
                    prompt_input, prompt_input_xpath = self._find_prompt_input_with_fallback(wait)

                    if prompt_input:
                        self._log(f"[{image_name}] Đã tìm thấy prompt input với selector: {prompt_input_xpath}")
                        try:
                            prompt_input.clear()
                            prompt_input.send_keys(image[self.excel_cols["prompt"]])
                            time.sleep(self.delays.get("after_prompt", 1))
                            self._log(f"[{image_name}] Đã nhập prompt: {image[self.excel_cols['prompt']]}")
                        except Exception as e:
                            self._log(f"[{image_name}] Lỗi khi nhập prompt: {e}")
                    else:
                        self._log(f"[{image_name}] Không tìm thấy prompt input với bất kỳ selector nào.")

                    # 5. Chờ trước khi remix
                    self._log(f"[{image_name}] Đang chờ {self.delays.get('before_remix', 5)} giây trước khi Remix...")
                    time.sleep(self.delays.get("before_remix", 5))

                    # 6. Tìm remix button và click
                    self._log(f"[{image_name}] Đang tìm remix button...")
                    self._log(f"[{image_name}] Trạng thái trang: {self._check_page_state()}")

                    remix_button, remix_button_xpath = self._find_remix_button_with_fallback(wait)

                    if not remix_button:
                        self._log(f"[{image_name}] Không tìm thấy remix button với bất kỳ selector nào. Bỏ qua ảnh này.")
                        continue

                    self._log(f"[{image_name}] Đã tìm thấy remix button với selector: {remix_button_xpath}")
                    self.driver.execute_script("arguments[0].click();", remix_button)
                    self._log(f"[{image_name}] Đã click nút Remix với ảnh và prompt.")

                    # 7. Chờ cố định sau khi bấm Remix (3 phút), sau đó tiếp tục ảnh tiếp theo
                    after_remix_delay = self.delays.get("after_remix", 180)
                    self._log(f"[{image_name}] Đang chờ {after_remix_delay} giây sau Remix, sau đó sẽ tiếp tục ảnh tiếp theo...")
                    time.sleep(after_remix_delay)

                    # 8. Hoàn thành ảnh hiện tại
                    self._log(f"[{image_name}] Hoàn thành xử lý ảnh. Sẽ chuyển sang ảnh tiếp theo.")

                    # Đánh dấu ảnh đã hoàn thành
                    df.loc[df[self.excel_cols["path"]] == image[self.excel_cols["path"]], self.excel_cols["status"]] = 'Completed'
                    save_success, save_message = self._safe_excel_save(df, excel_path)

                    if save_success:
                        self._log(f"[{image_name}] Xử lý thành công!")
                    else:
                        self._log(f"[{image_name}] Xử lý thành công nhưng không thể lưu Excel: {save_message}")

                    # Hoàn thành ảnh hiện tại, chuyển sang ảnh tiếp theo luôn
                    remaining_images = len(pending_images) - idx - 1
                    if remaining_images > 0:
                        self._log(f"[{image_name}] Hoàn thành! Còn {remaining_images} ảnh chưa xử lý. Bắt đầu ảnh tiếp theo...")
                    else:
                        self._log(f"[{image_name}] Đây là ảnh cuối cùng. Hoàn thành tất cả!")

                except Exception as e:
                    self._log(f"[{image_name}] Lỗi khi xử lý: {str(e)}")
                    self._log(f"[{image_name}] Trạng thái trang khi lỗi: {self._check_page_state()}")

                    # Đánh dấu ảnh bị lỗi
                    df.loc[df[self.excel_cols["path"]] == image[self.excel_cols["path"]], self.excel_cols["status"]] = f'Error: {str(e)[:50]}'
                    save_success, save_message = self._safe_excel_save(df, excel_path)

                    if not save_success:
                        self._log(f"[{image_name}] Không thể lưu trạng thái lỗi vào Excel: {save_message}")

                    continue
            return True, "Đã xử lý xong tất cả ảnh"
        except Exception as e:
            return False, f"Lỗi khi xử lý file excel: {str(e)}"

    def stop(self):
        self.is_running = False


# ==============================================================================
# PHẦN 2: GIAO DIỆN NGƯỜI DÙNG (ĐÃ ĐƯỢC CẬP NHẬT)
# ==============================================================================
class ChromeAutomationUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sora Automation v1 by Đạt0o ")
        self.root.geometry("800x750")

        self._setup_variables()
        self.automation = None
        self.sora = None

        self._create_widgets()
        self.log_message("Chương trình sẵn sàng. Vui lòng nhập các thông tin cần thiết.")

    def _setup_variables(self):
        """Khởi tạo các biến của Tkinter. Đã loại bỏ phần chọn profile."""
        self.chrome_path = tk.StringVar(value=CHROME_PATH)
        self.chrome_driver_path = tk.StringVar(value=CHROMEDRIVER_PATH)
        self.start_url = tk.StringVar(value=SORA_URL)
        self.image_folder = tk.StringVar(value=IMAGE_FOLDER)
        self.prompt_text = tk.StringVar(value=PROMPT)

        delays_cfg = DELAYS
        self.delay_after_upload = tk.DoubleVar(value=float(delays_cfg.get("after_upload", 10.0)))
        self.delay_after_prompt = tk.DoubleVar(value=float(delays_cfg.get("after_prompt", 1.0)))
        self.delay_before_remix = tk.DoubleVar(value=float(delays_cfg.get("before_remix", 1.0)))
        self.delay_after_remix = tk.DoubleVar(value=float(delays_cfg.get("after_remix", 180.0)))

        self.excel_file = tk.StringVar()
        self.status_var = tk.StringVar(value="Sẵn sàng")

    def _create_widgets(self):
        """Hàm chính, gọi các hàm con để tạo từng phần của giao diện."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._create_general_config_widgets(main_frame)
        self._create_sora_widgets(main_frame)
        self._create_delay_widgets(main_frame)
        self._create_control_widgets(main_frame)
        self._create_log_widgets(main_frame)
        self._create_status_bar(main_frame)

    def _create_general_config_widgets(self, parent):
        """Gộp phần cấu hình đường dẫn và cấu hình chung."""
        frame = ttk.LabelFrame(parent, text="1. Cấu hình chung", padding=10)
        frame.pack(fill=tk.X, pady=5)
        frame.columnconfigure(1, weight=1)

        # Đường dẫn Chrome
        ttk.Label(frame, text="Chrome Path:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.chrome_path).grid(row=0, column=1, sticky=tk.EW, padx=5)
        ttk.Button(frame, text="...", command=lambda: self._browse_file(self.chrome_path), width=4).grid(row=0,
                                                                                                         column=2)

        # Đường dẫn ChromeDriver
        ttk.Label(frame, text="ChromeDriver Path:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.chrome_driver_path).grid(row=1, column=1, sticky=tk.EW, padx=5)
        ttk.Button(frame, text="...", command=lambda: self._browse_file(self.chrome_driver_path), width=4).grid(row=1,
                                                                                                                column=2)

        # Start URL
        ttk.Label(frame, text="Start URL:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.start_url).grid(row=2, column=1, columnspan=2, sticky=tk.EW, padx=5)

    def _create_sora_widgets(self, parent):
        """Khu vực cấu hình cho tác vụ Sora."""
        frame = ttk.LabelFrame(parent, text="2. Cấu hình tác vụ", padding=10)
        frame.pack(fill=tk.X, pady=5)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Thư mục ảnh:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.image_folder).grid(row=0, column=1, sticky=tk.EW, padx=5)
        ttk.Button(frame, text="...", command=self._browse_folder, width=4).grid(row=0, column=2)

        ttk.Label(frame, text="Prompt chung:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.prompt_text).grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=5)

    def _create_delay_widgets(self, parent):
        """Khu vực cấu hình độ trễ."""
        frame = ttk.LabelFrame(parent, text="3. Cấu hình độ trễ (giây)", padding=10)
        frame.pack(fill=tk.X, pady=5)

        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

        ttk.Label(frame, text="Sau khi Upload:").grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        ttk.Entry(frame, textvariable=self.delay_after_upload, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(frame, text="Sau khi nhập Prompt:").grid(row=0, column=2, sticky=tk.W, pady=2, padx=5)
        ttk.Entry(frame, textvariable=self.delay_after_prompt, width=10).grid(row=0, column=3, sticky=tk.W, padx=5)

        ttk.Label(frame, text="Trước khi Remix:").grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
        ttk.Entry(frame, textvariable=self.delay_before_remix, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)

        ttk.Label(frame, text="Sau khi Remix:").grid(row=1, column=2, sticky=tk.W, pady=2, padx=5)
        ttk.Entry(frame, textvariable=self.delay_after_remix, width=10).grid(row=1, column=3, sticky=tk.W, padx=5)

    def _create_control_widgets(self, parent):
        """Khu vực các nút điều khiển chính."""
        frame = ttk.LabelFrame(parent, text="4. Điều khiển", padding=10)
        frame.pack(fill=tk.X, pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)

        buttons = {
            "Launch Chrome": self.launch_chrome,
            "Create Excel": self.create_excel,
            "Start Upload": self.start_upload,
            "Stop Upload": self.stop_upload,
            "Close Chrome": self.close_chrome
        }
        for text, command in buttons.items():
            ttk.Button(btn_frame, text=text, command=command).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

    def _create_log_widgets(self, parent):
        frame = ttk.LabelFrame(parent, text="Nhật ký hoạt động", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_text = scrolledtext.ScrolledText(frame, height=15, state=tk.DISABLED, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def _create_status_bar(self, parent):
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=2)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def log_message(self, message):
        log_entry = f"[{time.strftime('%H:%M:%S')}] {message}\n"
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)
        print(log_entry.strip())

    def _run_in_thread(self, target_func, *args):
        thread = threading.Thread(target=target_func, args=args, daemon=True)
        thread.start()

    def _browse_file(self, string_var):
        filename = filedialog.askopenfilename(title="Chọn file")
        if filename:
            string_var.set(filename)

    def _browse_folder(self):
        folder = filedialog.askdirectory(title="Chọn thư mục")
        if folder:
            self.image_folder.set(folder)

    def launch_chrome(self):
        self.log_message("Đang khởi động Chrome...")
        self.status_var.set("Launching Chrome...")

        def task():
            try:
                self.automation = ChromeProfileAutomation(self.chrome_path.get(), self.chrome_driver_path.get())
                headless = HEADLESS
                success, message = self.automation.launch_chrome_with_profile(
                    url=self.start_url.get(),
                    headless=headless
                )
                self.root.after(0, self.handle_launch_result, success, message)
            except Exception as e:
                self.root.after(0, self.handle_launch_result, False, str(e))

        self._run_in_thread(task)

    def handle_launch_result(self, success, message):
        self.log_message(message)
        if success and self.automation:
            self.status_var.set("Chrome đã sẵn sàng.")
            title = self.automation.get_page_title()
            url = self.automation.get_current_url()
            self.log_message(f"Trang hiện tại: {title} ({url})")
        else:
            self.status_var.set("Lỗi khởi chạy.")
            messagebox.showerror("Lỗi", message)

    def create_excel(self):
        folder = self.image_folder.get()
        if not folder:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục ảnh.")
            return

        user_prompt = self.prompt_text.get()
        if not user_prompt:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập prompt chung vào ô trống.")
            return

        excel_path = os.path.join(folder, EXCEL_FILENAME)
        self.excel_file.set(excel_path)

        sora_instance = self.sora if self.sora else SoraAutomation(driver=None)

        success, message = sora_instance.create_excel_from_folder(folder, excel_path, user_prompt)

        if success:
            self.log_message(message)
            messagebox.showinfo("Thành công", message)
        else:
            self.log_message(f"Lỗi: {message}")
            messagebox.showerror("Lỗi", message)

    def start_upload(self):
        if not self.automation or not self.automation.driver:
            messagebox.showerror("Lỗi", "Vui lòng khởi động Chrome trước.")
            return

        excel_path = self.excel_file.get()
        if not excel_path or not os.path.exists(excel_path):
            excel_path = os.path.join(self.image_folder.get(), EXCEL_FILENAME)
            if not os.path.exists(excel_path):
                messagebox.showerror("Lỗi", "Vui lòng tạo file excel trước.")
                return

        if not self.sora:
            self.sora = SoraAutomation(self.automation.driver)
        self.sora.set_ui(self)

        try:
            self.sora.delays["after_upload"] = float(self.delay_after_upload.get())
            self.sora.delays["after_prompt"] = float(self.delay_after_prompt.get())
            self.sora.delays["before_remix"] = float(self.delay_before_remix.get())
            self.sora.delays["after_remix"] = float(self.delay_after_remix.get())

            self.log_message(
                f"Đã cập nhật độ trễ: Sau Upload({self.sora.delays['after_upload']}s), Sau Prompt({self.sora.delays['after_prompt']}s), Trước Remix({self.sora.delays['before_remix']}s), Sau Remix({self.sora.delays['after_remix']}s)")
        except tk.TclError:
            messagebox.showerror("Lỗi giá trị", "Vui lòng nhập giá trị số hợp lệ cho các ô độ trễ.")
            return

        self.log_message("Bắt đầu quá trình upload...")
        self.status_var.set("Uploading...")
        self._run_in_thread(self.sora.process_images, excel_path)

    def stop_upload(self):
        if self.sora:
            self.sora.stop()
            self.log_message("Đã gửi yêu cầu dừng upload.")
            self.status_var.set("Đã dừng.")

    def close_chrome(self):
        if self.automation and hasattr(self.automation, 'close_chrome'):
            self.log_message("Đang đóng Chrome...")
            self.status_var.set("Closing Chrome...")
            result = self.automation.close_chrome()
            if isinstance(result, tuple) and len(result) == 2:
                success, message = result
            else:
                success, message = False, "Không thể đóng Chrome (hàm trả về không hợp lệ)"
            self.log_message(message)
            self.status_var.set("Đã đóng.")
            self.automation = None
            self.sora = None
        else:
            self.log_message("Không có phiên Chrome nào để đóng.")
            self.status_var.set("Không có Chrome.")

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.mainloop()

    def _on_closing(self):
        if self.automation:
            self.close_chrome()
        self.root.destroy()


if __name__ == "__main__":
    app = ChromeAutomationUI()
    app.run()
