from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('http://localhost:8080')
# time.sleep(10)
username = driver.find_element_by_name('login')
username.send_keys('eladk')
password = driver.find_element_by_name('password')
password.send_keys('1234')
password.send_keys(Keys.RETURN)

element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "newTaskButton"))
)
link = driver.find_element_by_id("newTaskButton")
link.click()
