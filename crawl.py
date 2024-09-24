from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager #webdriver-manager
import time

# chrome settings
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # 無頭模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

def crawl_cnyes(stock):
    # WebDriver init
    # target_stocks = ["TSLA", "META"]
    url = "https://invest.cnyes.com/usstock/detail/"
    target_url = url+stock

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    driver.get(target_url)
    time.sleep(2)

    date = None
    price = None

    try:
        # get the main element
        price_info_div = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".pure-g"))
        )

        # get the stock price and date
        date = price_info_div.find_element(
            By.CSS_SELECTOR, ".qmod-datetime-date"
        ).text
        close_price = price_info_div.find_element(By.CSS_SELECTOR, ".qmod-last").text
        close_price = float(close_price[1:])

        message = f"close price at date {date} is {close_price}"
        print(message)

    except Exception as e:
        print(f"發生錯誤: {e}")
    
    finally:
        return {"stock_symbol":stock, "price":close_price, "date":date}

if __name__=="__main__":
    target_stocks = ["TSLA", "META"]
    for stock in target_stocks:
        answer = crawl_cnyes(stock)
        print(answer)