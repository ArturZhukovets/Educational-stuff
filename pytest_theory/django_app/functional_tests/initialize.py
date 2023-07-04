import os
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium import webdriver

print(os.getcwd())
service = ChromeService(executable_path="chromedriver")

a = webdriver.Chrome(service=service)
print(a)
