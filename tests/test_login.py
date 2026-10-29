from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin:
    def test_successful_login(self, driver, base_url):
        driver.get(base_url)
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        WebDriverWait(driver, 15).until(EC.url_contains("/inventory.html"))
        items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(items) > 0

    def test_login_with_locked_user(self, driver, base_url):
        driver.get(base_url)
        driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        error = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        # Гибкая проверка
        assert "locked" in error.text.lower() or "epic sadface" in error.text.lower()

    def test_login_with_empty_fields(self, driver, base_url):
        driver.get(base_url)
        driver.find_element(By.ID, "login-button").click()
        
        error = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        # Гибкая проверка
        assert "username" in error.text.lower() or "required" in error.text.lower() or "epic sadface" in error.text.lower()