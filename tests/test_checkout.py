import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCheckout:
    """Тесты процесса оформления заказа"""
    
    def login_as_standard_user(self, driver, base_url):
        """Вспомогательный метод для входа в систему"""
        driver.get(base_url)
        
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains("/inventory.html")
        )
    
    def test_add_item_to_cart(self, driver, base_url):
        """Тест добавления товара в корзину"""
        self.login_as_standard_user(driver, base_url)
        
        # Добавление товара "Backpack" в корзину
        add_to_cart_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_to_cart_button.click()
        
        # Проверка появления значка корзины
        cart_badge = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        
        assert cart_badge.text == "1", "Счетчик корзины не равен 1"
    
    def test_complete_checkout_process(self, driver, base_url):
        """Тест полного процесса оформления заказа"""
        self.login_as_standard_user(driver, base_url)
        
        # Добавление товара в корзину
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        
        # Переход в корзину
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        
        # Проверка наличия товара в корзине
        cart_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item"))
        )
        assert len(cart_items) > 0, "Корзина пуста"
        
        # Переход к оформлению заказа
        driver.find_element(By.ID, "checkout").click()
        
        # Заполнение формы доставки
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()
        
        # Проверка страницы подтверждения заказа
        total_label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='total-label']"))
        )
        assert "Total" in total_label.text
        
        # Завершение заказа
        driver.find_element(By.ID, "finish").click()
        
        # Проверка страницы успешного завершения
        complete_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        assert "Thank you for your order!" in complete_header.text