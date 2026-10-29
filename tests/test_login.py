import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogin:
    """Тесты страницы авторизации"""
    
    def test_successful_login(self, driver, base_url):
        """Тест успешного входа в систему"""
        driver.get(base_url)
        
        # Ввод данных для входа
        username_field = driver.find_element(By.ID, "user-name")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        login_button.click()
        
        # Проверка перехода на страницу каталога
        WebDriverWait(driver, 10).until(
            EC.url_contains("/inventory.html")
        )
        
        # Проверка наличия элементов каталога
        inventory_items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(inventory_items) > 0, "Каталог товаров пуст"
    
    def test_login_with_locked_user(self, driver, base_url):
        """Тест входа с заблокированным пользователем"""
        driver.get(base_url)
        
        # Ввод данных заблокированного пользователя
        username_field = driver.find_element(By.ID, "user-name")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")
        
        username_field.send_keys("locked_out_user")
        password_field.send_keys("secret_sauce")
        login_button.click()
        
        # Проверка отображения ошибки
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        
        assert "Epic sadface: Sorry, this user has been locked out." in error_message.text
    
    def test_login_with_empty_fields(self, driver, base_url):
        """Тест входа с пустыми полями"""
        driver.get(base_url)
        
        # Попытка входа без ввода данных
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Проверка отображения ошибки
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        
        assert "Username is required" in error_message.text