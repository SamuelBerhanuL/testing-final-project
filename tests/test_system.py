# tests/test_system.py
import pytest
import threading
from werkzeug.serving import make_server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from app import app
from tests.pages.shop_page import ShopPage

# This fixture runs the Flask app in the background while Selenium tests it
class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

@pytest.fixture(scope="module")
def live_server():
    server = ServerThread(app)
    server.start()
    yield server
    server.shutdown()

@pytest.fixture
def browser():
    chrome_options = Options()
    # We use headless mode so it doesn't pop up a visible window during automated tests
    chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_user_journey(live_server, browser):
    """System Test: End-to-End User Journey using Page Object Pattern"""
    shop = ShopPage(browser)
    shop.load()
    
    # 1. Verify Initial State
    assert shop.get_state() == "cart"
    
    # 2. Add an item below the free shipping boundary ($40 + $10 shipping = $50)
    shop.add_item("40.00")
    assert shop.get_total() == "50.0"
    
    # 3. Checkout and transition state
    shop.checkout()
    
    # 4. Verify Final State
    assert "placed" in browser.page_source
