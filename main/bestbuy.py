import time
import sys
from random import randrange

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from notification.sms import SMSNotify

# Give selenium image time to load up
if sys.argv[1] == "remote":
    time.sleep(3)


class ShoppingBot:
    def __init__(self):
        self.refresh_timer = randrange(3, 9)
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        if sys.argv[1] == "remote":
            self.driver = webdriver.Remote("http://selenium:4444/wd/hub",
                                           desired_capabilities=DesiredCapabilities.CHROME,
                                           options=chrome_options)
        else:
            self.driver = webdriver.Chrome(options=chrome_options)
        self.store = "Best Buy"
        self.driver.get("https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149")

        # Test url to verify working
        # self.driver.get("https://www.bestbuy.com/site/insignia-3-3-5mm-audio-cable-black/5019113.p?skuId=5019113")

    def checkout(self):
        self.driver.get("https://www.bestbuy.com/cart")
        time.sleep(3)
        checkout = self.driver.find_elements_by_class_name("btn-primary")[0]
        checkout.click()

    def wait(self):
        wait = randrange(1, 6)
        time.sleep(wait)
        self.driver.refresh()

    def reset_timer(self):
        self.refresh_timer = randrange(3, 9)
        long_sleep = randrange(10, 90)
        print("Sleeping for " + str(long_sleep) + " seconds")
        time.sleep(long_sleep)

    def add_to_cart(self):
        button = self.driver.find_element_by_class_name("add-to-cart-button")
        is_disabled = "btn-disabled" in button.get_attribute("class")
        if is_disabled:
            return False
        else:
            button.click()
            return True

    def __del__(self):
        self.driver.close()


if __name__ == "__main__":
    shopping_bot = ShoppingBot()
    sms = SMSNotify()

    found_item = False
    try:
        while not found_item:
            if shopping_bot.refresh_timer <= 0:
                shopping_bot.reset_timer()
            if shopping_bot.add_to_cart():
                found_item = True
                sms.message(shopping_bot.store)
                print("Added to cart!")
                break
            shopping_bot.refresh_timer -= 1
            shopping_bot.wait()
    # Any issues happen to shopping bot.
    except:
        sms.message(shopping_bot.store, error=True)
        print("Shopping bot had an error.")
    shopping_bot.checkout()

    # Leave time to manually finish transaction if successful
    time.sleep(3600)
