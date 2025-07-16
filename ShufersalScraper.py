import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ShufersalScraper:
    def __init__(self, headless=False):
        self.log_path = self.get_log_path()
        self.log(f"Log started: {datetime.now().isoformat()}")
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.driver = None

    def get_log_path(self):
        os.makedirs('logs', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join('logs', f'run_{timestamp}.log')

    def log(self, msg):
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')

    def _start_driver(self):
        try:
            self.driver = webdriver.Chrome(options=self.options)
            self.log("Chrome WebDriver started successfully.")
        except Exception as e:
            self.log(f"Failed to start Chrome WebDriver: {e}")
            raise

    def _stop_driver(self):
        if self.driver:
            self.driver.quit()
            self.log("Chrome WebDriver closed.")

    def search_product(self, product_search_name, quantity):
        """
        input:
            product_search_name: str
            quantity: int
        output:
            list of raw htmls
        """
        self._start_driver()
        try:
            # Build search URL
            from urllib.parse import quote
            search_term = quote(product_search_name)
            url = f"https://www.shufersal.co.il/online/he/search?text={search_term}"
            self.log(f"Navigating to URL: {url}")
            self.driver.get(url)
            time.sleep(2)
            self.log("Page loaded, fetching HTML.")
            html = self.driver.page_source
            # Save HTML for debugging
            with open('logs/last_page.html', 'w', encoding='utf-8') as f:
                f.write(html)
            soup = BeautifulSoup(html, 'html.parser')
            # Find all product tiles
            products = soup.find_all('li', class_=lambda c: c and 'miglog-prod' in c)
            if not products:
                self.log("ERROR: No product tiles found with 'miglog-prod' in class!")
                return []
            else:
                self.log(f"Found {len(products)} product tiles.")
            # Return up to 'quantity' raw HTMLs
            raw_htmls = [str(prod) for prod in products[:quantity]]
            for i, raw_html in enumerate(raw_htmls):
                self.log(f"\n--- Product {i+1} Raw HTML ---\n{raw_html}\n")
            return raw_htmls
        finally:
            self._stop_driver()
