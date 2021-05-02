import time
from random import randrange

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from notification.sms import SMSNotify


class ShoppingBot:
    def __init__(self):
        self.refresh_timer = randrange(3, 9)
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver.get("https://www.target.com/p/playstation-5-console/-/A-81114595#lnk=sametab")
        # self.driver.get("https://www.target.com/p/dualsense-wireless-controller-for-playstation-5/-/A-81114477")
        self.driver.get("https://www.target.com/p/xbox-gift-card-digital/-/A-53054514?preselect=52567882#lnk=sametab")

    def checkout(self):
        self.driver.get("https://www.target.com/co-cart")
        time.sleep(3)
        # checkout = self.driver.find_elements_by_class_name("btn-primary")[0]
        # checkout.click()

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
        try:
            button = self.driver.find_elements_by_css_selector("button.Button__ButtonWithStyles-sc-1a5r2pb-0.etCdMB")
            button.click()
            return True
        except:
            print("Could not find button")
            return False
        # is_disabled = "btn-disabled" in button.get_attribute("class")
        # if is_disabled:
        #     return False
        # else:
        #     button.click()
        #     return True

    def __del__(self):
        self.driver.close()


if __name__ == "__main__":
    shopping_bot = ShoppingBot()
    found_item = False
    while not found_item:
        if shopping_bot.refresh_timer <= 0:
            shopping_bot.reset_timer()
        if shopping_bot.add_to_cart():
            found_item = True
            sms = SMSNotify()
            # sms.message("Target")
            print("Added to cart!")
            break
        shopping_bot.refresh_timer -= 1
        shopping_bot.wait()
    shopping_bot.checkout()

    time.sleep(2000)
