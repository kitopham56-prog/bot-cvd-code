import os
import time
import schedule
import requests
from datetime import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import io
import base64
from PIL import Image

class HashweiTelegramBot:
    def __init__(self):
        self.bot_token = "8372904645:AAFso89K2UabIdYZ2HZrRGhV8xD41kmaZWA"
        self.group_id = "-1002845367780"
        self.hashwei_url = "https://hashwei.ai/dashboard/cvd"
        self.driver = None
        self.vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        
    def setup_driver(self):
        """Thiết lập Chrome driver với các options phù hợp cho Render"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Tắt load ảnh để tăng tốc
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(60)
            print("✅ Chrome driver đã được thiết lập thành công")
            return True
        except Exception as e:
            print(f"❌ Lỗi thiết lập driver: {e}")
            return False
    
    def wait_for_element(self, by, value, timeout=30):
        """Chờ element xuất hiện"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"⏰ Timeout chờ element: {value}")
            return None
    
    def wait_for_clickable(self, by, value, timeout=30):
        """Chờ element có thể click"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            print(f"⏰ Timeout chờ clickable element: {value}")
            return None
    
    def navigate_to_hashwei(self):
        """Điều hướng đến trang Hashwei"""
        try:
            print("🌐 Đang truy cập Hashwei...")
            self.driver.get(self.hashwei_url)
            
            # Chờ trang load
            time.sleep(10)
            
            # Kiểm tra xem có cần đăng nhập không
            if "login" in self.driver.current_url.lower():
                print("🔐 Cần đăng nhập...")
                time.sleep(5)  # Chờ form đăng nhập load
            
            # Chờ dashboard load hoàn tất
            print("⏳ Chờ dashboard load...")
            time.sleep(15)
            
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi truy cập Hashwei: {e}")
            return False
    
    def navigate_to_cvd_section(self):
        """Điều hướng đến phần CVD"""
        try:
            print("📊 Đang điều hướng đến phần CVD...")
            
            # Tìm và click Data Off Chain
            data_offchain_selectors = [
                "//a[contains(text(), 'Data Off Chain')]",
                "//button[contains(text(), 'Data Off Chain')]",
                "//div[contains(text(), 'Data Off Chain')]",
                "[data-testid*='offchain']",
                ".menu-item:contains('Data Off Chain')",
                "*[title*='Data Off Chain']"
            ]
            
            data_offchain_clicked = False
            for selector in data_offchain_selectors:
                try:
                    if selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        element.click()
                        print("✅ Đã click Data Off Chain")
                        data_offchain_clicked = True
                        time.sleep(5)
                        break
                except:
                    continue
            
            if not data_offchain_clicked:
                print("⚠️ Không tìm thấy Data Off Chain, tiếp tục...")
            
            # Tìm và click OrderFlow Heatmap
            heatmap_selectors = [
                "//a[contains(text(), 'OrderFlow') or contains(text(), 'Heatmap')]",
                "//button[contains(text(), 'OrderFlow') or contains(text(), 'Heatmap')]",
                "[data-testid*='heatmap']",
                ".menu-item:contains('Heatmap')",
                "*[title*='Heatmap']"
            ]
            
            heatmap_clicked = False
            for selector in heatmap_selectors:
                try:
                    if selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        element.click()
                        print("✅ Đã click OrderFlow Heatmap")
                        heatmap_clicked = True
                        time.sleep(5)
                        break
                except:
                    continue
            
            if not heatmap_clicked:
                print("⚠️ Không tìm thấy OrderFlow Heatmap, tiếp tục...")
            
            # Tìm và click Absolute CVD
            cvd_selectors = [
                "//a[contains(text(), 'Absolute CVD') or contains(text(), 'CVD')]",
                "//button[contains(text(), 'Absolute CVD') or contains(text(), 'CVD')]",
                "[data-testid*='cvd']",
                ".menu-item:contains('CVD')",
                "*[title*='CVD']"
            ]
            
            for selector in cvd_selectors:
                try:
                    if selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        element.click()
                        print("✅ Đã click Absolute CVD")
                        time.sleep(10)  # Chờ CVD load
                        break
                except:
                    continue
            
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi điều hướng đến CVD: {e}")
            return False
    
    def select_ticker_and_capture(self, ticker):
        """Chọn ticker và chụp màn hình"""
        try:
            print(f"🎯 Đang chọn ticker: {ticker}")
            
            # Tìm và click ticker
            ticker_selectors = [
                f"//button[contains(text(), '{ticker}')]",
                f"//div[contains(text(), '{ticker}')]",
                f"//option[contains(text(), '{ticker}')]",
                f"[data-value='{ticker}']",
                f"[value='{ticker}']",
                f".ticker-option:contains('{ticker}')"
            ]
            
            ticker_selected = False
            for selector in ticker_selectors:
                try:
                    if selector.startswith("//"):
                        element = self.driver.find_element(By.XPATH, selector)
                    else:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if element.is_displayed():
                        element.click()
                        print(f"✅ Đã chọn {ticker}")
                        ticker_selected = True
                        time.sleep(8)  # Chờ data load
                        break
                except:
                    continue
            
            if not ticker_selected:
                # Thử tìm dropdown/select để chọn ticker
                try:
                    dropdown_selectors = [
                        "//select",
                        ".dropdown",
                        ".select",
                        "[role='combobox']"
                    ]
                    
                    for dropdown_selector in dropdown_selectors:
                        try:
                            if dropdown_selector.startswith("//"):
                                dropdown = self.driver.find_element(By.XPATH, dropdown_selector)
                            else:
                                dropdown = self.driver.find_element(By.CSS_SELECTOR, dropdown_selector)
                            
                            dropdown.click()
                            time.sleep(2)
                            
                            # Tìm option với ticker
                            option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{ticker}')]")
                            option.click()
                            print(f"✅ Đã chọn {ticker} từ dropdown")
                            ticker_selected = True
                            time.sleep(8)
                            break
                        except:
                            continue
                except:
                    pass
            
            if not ticker_selected:
                print(f"⚠️ Không tìm thấy ticker {ticker}, sẽ chụp màn hình hiện tại")
            
            # Chờ thêm để đảm bảo data đã load
            time.sleep(5)
            
            # Chụp màn hình
            screenshot = self.driver.get_screenshot_as_png()
            
            return screenshot
            
        except Exception as e:
            print(f"❌ Lỗi khi chọn ticker {ticker}: {e}")
            return None
    
    def send_telegram_photo(self, photo_data, caption):
        """Gửi ảnh lên Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
            
            files = {
                'photo': ('screenshot.png', photo_data, 'image/png')
            }
            
            data = {
                'chat_id': self.group_id,
                'caption': caption,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                print("✅ Đã gửi ảnh lên Telegram thành công")
                return True
            else:
                print(f"❌ Lỗi gửi ảnh: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi khi gửi Telegram: {e}")
            return False
    
    def get_vietnam_time(self):
        """Lấy thời gian Việt Nam"""
        return datetime.now(self.vietnam_tz).strftime("%d/%m/%Y %H:%M:%S")
    
    def scan_and_post(self):
        """Thực hiện scan và đăng bài"""
        try:
            print(f"🚀 Bắt đầu scan lúc: {self.get_vietnam_time()}")
            
            # Setup driver
            if not self.setup_driver():
                return False
            
            # Truy cập Hashwei
            if not self.navigate_to_hashwei():
                return False
            
            # Điều hướng đến CVD
            if not self.navigate_to_cvd_section():
                return False
            
            # Scan BTCUSDT
            print("📸 Đang scan BTCUSDT...")
            btc_screenshot = self.select_ticker_and_capture("BTCUSDT")
            
            if btc_screenshot:
                btc_caption = f"""
🪙 <b>Coin:</b> BTCUSDT
⏰ <b>Thời gian cập nhật:</b> {self.get_vietnam_time()}
📊 <b>Dữ liệu:</b> Hashwei CVD Heatmap

#BTCUSDT #Hashwei #CVD
"""
                self.send_telegram_photo(btc_screenshot, btc_caption)
                time.sleep(3)  # Chờ giữa các lần gửi
            
            # Scan ETHUSDT
            print("📸 Đang scan ETHUSDT...")
            eth_screenshot = self.select_ticker_and_capture("ETHUSDT")
            
            if eth_screenshot:
                eth_caption = f"""
🪙 <b>Coin:</b> ETHUSDT
⏰ <b>Thời gian cập nhật:</b> {self.get_vietnam_time()}
📊 <b>Dữ liệu:</b> Hashwei CVD Heatmap

#ETHUSDT #Hashwei #CVD
"""
                self.send_telegram_photo(eth_screenshot, eth_caption)
            
            print("✅ Hoàn thành scan!")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi trong quá trình scan: {e}")
            return False
            
        finally:
            # Đóng driver
            if self.driver:
                self.driver.quit()
                self.driver = None
    
    def start_bot(self):
        """Khởi động bot"""
        print("🤖 Khởi động Hashwei Telegram Bot...")
        print(f"⏰ Bot sẽ scan mỗi giờ, bắt đầu từ: {self.get_vietnam_time()}")
        
        # Chạy lần đầu ngay lập tức
        self.scan_and_post()
        
        # Lên lịch chạy mỗi giờ
        schedule.every().hour.at(":00").do(self.scan_and_post)
        
        print("⏰ Bot đang chạy, sẽ scan mỗi giờ...")
        print("🛑 Nhấn Ctrl+C để dừng bot")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Kiểm tra mỗi phút
            except KeyboardInterrupt:
                print("🛑 Bot đã được dừng!")
                if self.driver:
                    self.driver.quit()
                break
            except Exception as e:
                print(f"❌ Lỗi trong vòng lặp chính: {e}")
                time.sleep(300)  # Chờ 5 phút trước khi thử lại

if __name__ == "__main__":
    bot = HashweiTelegramBot()
    bot.start_bot()
