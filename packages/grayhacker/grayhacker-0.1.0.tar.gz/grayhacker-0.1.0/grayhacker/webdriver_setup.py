from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class GrayHacker:
    def __init__(self):
        self.driver = self._init_driver()

    @staticmethod
    def _init_driver():
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")  # Bỏ dòng này nếu muốn giao diện
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1000, 812)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
