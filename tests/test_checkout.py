from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCheckout:

    def login(self, driver, base_url):
        driver.get(base_url)
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        WebDriverWait(driver, 15).until(EC.url_contains("/inventory.html"))

    def test_add_item_to_cart(self, driver, base_url):
        self.login(driver, base_url)
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        
        badge = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        assert badge.text == "1"

    def test_complete_checkout_process(self, driver, base_url):
        self.login(driver, base_url)
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        
        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()
        
        total = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='total-label']"))
        )
        assert "Total" in total.text
        
        driver.find_element(By.ID, "finish").click()
        
        header = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        assert "Thank you" in header.text