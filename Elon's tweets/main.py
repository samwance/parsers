from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_tweets():
    driver = webdriver.Chrome()

    # Открытие страницы с твитами пользователя
    driver.get("https://twitter.com/elonmusk")
    driver.maximize_window()

    # Ожидание загрузки кнопки "Принять все файлы cookie"
    wait = WebDriverWait(driver, 10)

    time.sleep(5)

    # Ожидание загрузки твитов
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1rynq56.r-8akbws.r-krxsd3.r-dnmrzs.r-1udh08x.r-bcqeeo.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-16dba41.r-bnwqim")))

    # Скроллинг и сбор твитов
    # Прокрутка страницы
    scroll_script = """
    const scrollBy = (amount) => {
      window.scrollBy(0, amount);
    };

    const interval = setInterval(() => {
      scrollBy(50); // Прокрутка на 50 пикселей

      // Проверка, достигли ли мы конца страницы
      if (window.innerHeight + window.scrollY >= document.body.scrollHeight) {
        clearInterval(interval); // Остановка интервала
      }
    }, 100); // Интервал 100 мс
    """

    # Выполнение JavaScript-кода
    driver.execute_script(scroll_script)
    time.sleep(3)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1rynq56.r-8akbws.r-krxsd3.r-dnmrzs.r-1udh08x.r-bcqeeo.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-16dba41.r-bnwqim")))

    tweets = driver.find_elements(By.CSS_SELECTOR,
                                  ".css-1rynq56.r-8akbws.r-krxsd3.r-dnmrzs.r-1udh08x.r-bcqeeo.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-16dba41.r-bnwqim")

    # Вывод текста всех твитов
    for tweet in tweets[:10]:
        if tweet.is_displayed():
            if tweet.text.strip():
                # Вывод текста твита
                print(tweet.text)
            else:
                print('твит без текста')

    # Закрытие браузера
    driver.quit()


if __name__ == "__main__":
    get_tweets()
