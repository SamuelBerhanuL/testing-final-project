# tests/pages/shop_page.py
from selenium.webdriver.common.by import By

class ShopPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://127.0.0.1:5000"
        
        # Locators
        self.price_input = (By.ID, "price-input")
        self.add_btn = (By.ID, "add-btn")
        self.checkout_btn = (By.ID, "checkout-btn")
        self.total_span = (By.ID, "order-total")
        self.state_span = (By.ID, "order-state")

    def load(self):
        self.driver.get(self.url)

    def add_item(self, price):
        self.driver.find_element(*self.price_input).clear()
        self.driver.find_element(*self.price_input).send_keys(str(price))
        self.driver.find_element(*self.add_btn).click()

    def checkout(self):
        self.driver.find_element(*self.checkout_btn).click()

    def get_total(self):
        return self.driver.find_element(*self.total_span).text

    def get_state(self):
        return self.driver.find_element(*self.state_span).text
