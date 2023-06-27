import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("http://185.67.95.60/")
    yield driver
    driver.delete_all_cookies()
    driver.close()


# Автоматический ввод данных для авторизации
def auth_data(driver):
    login = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.ID, "loginEmail")))
    login.send_keys('test@protei.ru')

    password = driver.find_element(by=By.XPATH, value="//input[@type='password']")
    password.send_keys('test')

    enter = driver.find_element(by=By.CSS_SELECTOR, value=".uk-button")
    enter.click()


# Тест №1. Авторизация с корректными входными данными
def test_auth_valid(driver):
    auth_data(driver)

    main_title = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.TAG_NAME, "h3")))

    assert True
    assert main_title.is_displayed()
    assert main_title.get_attribute("class") == "uk-card-title"
    assert main_title.text == "Добро пожаловать!"


# Тест №2. Переход на раздел "Варианты"
def test_go_to_variants(driver):
    auth_data(driver)

    enter = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.ID, "menuMore")))
    enter.click()

    variants_title = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.TAG_NAME, "h3")))

    assert True
    assert variants_title.is_displayed()
    assert variants_title.get_attribute("class") == "uk-card-title"
    assert variants_title.text == "НТЦ ПРОТЕЙ"


# Тест №3. Добавление пользователя
def test_add_user(driver):
    auth_data(driver)

    click_users = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.ID, "menuUsersOpener")))
    click_users.click()
    click_users.click()

    click_add_user = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.ID, "addUser")))
    click_add_user.click()

    login = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.ID, "dataEmail")))
    login.send_keys('lol@kek')

    password = driver.find_element(by=By.ID, value="dataPassword")
    password.send_keys('cheburek')

    name = driver.find_element(by=By.ID, value="dataName")
    name.send_keys('cheburek')

    click_add = driver.find_element(by=By.ID, value="dataSend")
    click_add.click()

    data_added = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".uk-modal-body")))

    assert True
    assert data_added.is_displayed()
    assert data_added.get_attribute("class") == "uk-modal-body"
    assert data_added.text == "Данные добавлены."
