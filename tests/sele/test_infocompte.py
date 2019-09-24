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
driver.find_element(By.LINK_TEXT, "Se connecter").click()
driver.find_element(By.ID, "exampleInputMail").click()
driver.find_element(By.ID, "exampleInputMail").send_keys("testselenium@hotmail.fr")
driver.find_element(By.ID, "exampleInputPassword").click()
driver.find_element(By.ID, "exampleInputPassword").send_keys("testselenium")
driver.find_element(By.CSS_SELECTOR, ".float-right").click()
driver.find_element(By.LINK_TEXT, "Mon compte").click()

inputname = driver.find_element_by_id('exampleInputName')
print(inputname.getAttribute("value"))
if "testselenium" not in inputname.get_value("testselenium"):
    raise Exception("Not the right name for this account!")
driver.quit()  

  
