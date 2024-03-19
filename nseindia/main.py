
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import re

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_table():
    driver = webdriver.Chrome()
    driver.get('https://www.nseindia.com/')
    time.sleep(3)

    # находим market data по тексту
    market_data = driver.find_element(By.XPATH, "//a[contains(text(), 'Market Data')]")

    # наводим курсор
    ActionChains(driver).move_to_element(market_data).perform()

    # "pre-open arket" по тексту
    pre_open_market = driver.find_element(By.XPATH, "//a[contains(text(), 'Pre-Open Market')]")

    # кликаем
    pre_open_market.click()
    time.sleep(10)

    # все строки в таблице:
    rows = driver.find_elements(By.XPATH, "//tbody/tr")

    # CSV-файл
    with open('nseindia_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Имя', 'Цена'])

        # Записать данные из каждой строки
        for row in rows:
            name = row.find_element(By.XPATH, "./td[2]").text
            price = row.find_element(By.XPATH, "./td[7]").text

            # убрал последнюю строчку с Total
            if not price:
                break

            # оставляем только цифры
            price = re.sub(r'\D', '', price)

            writer.writerow([name, price])

    driver.quit()


def imitate_the_user():
    driver = webdriver.Chrome()
    driver.get('https://www.nseindia.com/')
    driver.maximize_window()
    time.sleep(3)

    # Нажимаем на ссылку "QUICK LINKS"
    quick_link = driver.find_element(By.CSS_SELECTOR, "a[onclick='getNifty50Data()']")
    quick_link.click()
    time.sleep(2)

    # Нажимаем на кнопку NIFTY BANK
    nifty_bank = driver.find_element(By.XPATH, "//p[contains(text(), 'NIFTY BANK')]")
    nifty_bank.click()
    time.sleep(3)

    # Находим кнопку View All
    element = driver.find_element(By.CSS_SELECTOR, "div.link-wrap a[href='/market-data/live-equity-market?symbol=NIFTY BANK']")

    # ActionChains
    actions = ActionChains(driver)

    # Наводим на кнопку
    actions.move_to_element(element).perform()
    actions.click(element).perform()
    time.sleep(10)

    # Находим селектор
    select_element = driver.find_element(By.ID, "equitieStockSelect")
    select_element.click()
    time.sleep(2)

    # ыбираем нужный вариант
    select = Select(select_element)
    select.select_by_value("NIFTY ALPHA 50")
    time.sleep(10)

    # Последняя строчка в таблице
    target_row = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody/tr[last()]")))

    driver.execute_script("arguments[0].scrollIntoView();", target_row)

    driver.quit()


if __name__ == '__main__':
    choice = input('Выберите вариант: \n1 - Спарсить данные из таблицы \n2 - Сымитировать поведение пользователя\n')
    if choice == '1':
        parse_table()
    elif choice == '2':
        imitate_the_user()
