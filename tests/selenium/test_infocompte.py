# Selenium 3.14+ doesn't enable certificate checking
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

desired_cap = {
    'platform': "Mac OS X 10.13",
    'browserName': "safari",
    'version': "11.1",
    'build': "Onboarding Sample App - Python",
    'name': "2-user-site",
}
username = os.environ["SAUCE_USERNAME"]
access_key = os.environ["SAUCE_ACCESS_KEY"]
driver = webdriver.Remote(
   command_executor='https://{}:{}@ondemand.eu-central-1.saucelabs.com/wd/hub'.format(username, access_key),
   desired_capabilities=desired_cap)

driver.get("https://find-your-nest-ywhzbcfbpq-ew.a.run.app/")
time.sleep(2)
driver.find_element(By.LINK_TEXT, "Se connecter").click()
driver.find_element(By.ID, "exampleInputMail").click()
driver.find_element(By.ID, "exampleInputMail").send_keys("lola@gmail.com")
driver.find_element(By.ID, "exampleInputMail").send_keys(Keys.DOWN)
driver.find_element(By.ID, "exampleInputMail").send_keys(Keys.TAB)
driver.find_element(By.ID, "exampleInputPassword").send_keys("lola")
driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(4)").click()

if "Find Your Nest" not in driver.title:
    raise Exception("Unable to load saucedemo page!")
driver.quit()
