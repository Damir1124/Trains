import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import traceback
from webdriver_manager.chrome import ChromeDriverManager

class ProductChecker:
    def __init__(self):
        self.driver = None
        self.driver_options = None

    async def start_driver(self, url):
        try:
            self.driver_options = webdriver.ChromeOptions()
            # self.driver_options.add_argument('--headless')  # Добавляем параметр для headless-режима
            self.driver_options.add_argument("--disable-blink-features=AutomationControlled")
            self.driver_options.add_argument('--start-maximized')

            # Инициализация драйвера перед использованием
            self.driver = webdriver.Chrome(options=self.driver_options)


            # Переносим execute_cdp_cmd после инициализации драйвера
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                'source': '''
                    cdc_adoQpoasnfa76pfcZimcfl Array;
                    cde_adoQpoasnfa76pfcZimcfl_Promise;
                    cdc_adoQpoasnfa76pfczimcfl_ Symbol;
                    '''
            })

            self.driver.get(url)
            await asyncio.sleep(4)

        except Exception as e:
            print(e)
    async def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.driver_options = None

    async def get_product_values(self, product_card_url):
        try:
            await self.start_driver(product_card_url)
            wait = WebDriverWait(self.driver, 10)

            main_characteristics = wait.until(
                EC.visibility_of_element_located((By.XPATH, """//*[@id="product-info"]"""))
            )

            if main_characteristics:
                rating = re.sub(r'[^0-9.]', '', main_characteristics.find_element(By.CLASS_NAME, """rating-value""").text)
                grades = re.sub(r'[^0-9]', '', main_characteristics.find_element(By.CLASS_NAME, """dotted""").text)
                orders = re.sub(r'[^0-9]', '', main_characteristics.find_element(By.CLASS_NAME, """orders""").text)
                title = main_characteristics.find_element(By.CLASS_NAME, """title""").text
                values = re.sub(r'[^0-9]', '', main_characteristics.find_element(By.XPATH,
                                            """//*[@id="product-info"]/div[2]/div[4]/div[2]/div[2]/span""").text)

                return f"Наименование: {title}\nРейтинг: {rating}\nФидбек: {grades}\nВсего продаж: {orders}\nВ наличии: {values}\n"
            else:
                print("[ERROR] main_characteristics is None")
                return "Сайт не ответил"

        except Exception as e:
            print(f"[ERROR] {e}")
            return "Сайт не ответил"
        finally:
            await self.close_driver()

    async def markup(self, url, time):
        for _ in range(25):
            await asyncio.sleep(time)
            data = await self.get_product_values(url)
            return data

    async def all_positions(self):
        try:
            await self.start_driver("https://uzum.uz/ru/category/vse-kategorii-1")
            wait = WebDriverWait(self.driver, 10)

            all_positions = wait.until(
                EC.visibility_of_element_located((By.XPATH, """//*[@id="category-content"]/div[1]/div[1]/div[2]"""))
            )

            if all_positions:
                return (f"{all_positions.text} на маркетплейсе")
            else:
                print("[ERROR] main_characteristics is None")
                return "Сайт не ответил"

        except Exception as e:
            print(f"[ERROR] {e}")
            return "Сайт не ответил"

        finally:
            await self.close_driver()



# if __name__ == '__main__':
#     product_checker = ProductChecker()
#     asyncio.run(product_checker.get_product_values('https://uzum.uz/uz/product/pemza-oyoqlar-uchun-qirgichlari-ikki-tomonlama-35382'))

