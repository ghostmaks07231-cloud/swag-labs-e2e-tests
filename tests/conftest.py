import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания и настройки WebDriver"""
    chrome_options = Options()
    
    # Для GitHub Actions используем headless режим
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Установка ChromeDriver через webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Неявное ожидание элементов
    driver.implicitly_wait(10)
    
    yield driver
    
    # Закрытие браузера после теста
    driver.quit()


@pytest.fixture(scope="function")
def base_url():
    """Базовый URL приложения"""
    return "https://www.saucedemo.com"