import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import json
from settings import settings
from getEmailCode import get_email_code
from getDataFromPage import get_data_from_page


chrome_options = Options()
chrome_options.add_argument(f"--proxy-server=http://{settings['proxies']}")
browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

browser.get("https://www.linkedin.com/")  # login
username = browser.find_element(By.ID, "session_key")
password = browser.find_element(By.ID, "session_password")
username.send_keys(settings["linkedin"]["email"])  # should be in .env file
password.send_keys(settings["linkedin"]["password"])  # should be in .env file
browser.find_element(By.CLASS_NAME, "sign-in-form__submit-button").click()
try:
    email_check = browser.find_element(By.ID, "input__email_verification_pin")
    email_check.send_keys(get_email_code())
    browser.find_element(By.ID, "email-pin-submit-button").click()
except selenium.common.exceptions.NoSuchElementException:
    pass

current_page = 1
search_url = "https://www.linkedin.com/search/results/people/?" \
             "origin=FACETED_SEARCH&schoolFilter=%5B%2215151368%22%5D&sid=n*n?page="
browser.get(search_url + str(current_page))  # searching urls of MISIS graduates
# pages = browser.find_element(By.CSS_SELECTOR, "ul.artdeco-pagination__pages.artdeco-pagination__pages--number")
# pages_count = int(pages[-1].text)
pages_count = 10
data = []
for current_page in range(2, pages_count + 1):
    students_from_misis = browser.find_elements(By.CLASS_NAME, "reusable-search__result-container")
    for student in students_from_misis:
        student.find_element(By.CLASS_NAME, "app-aware-link").click()
        try:
            personal_data = browser.find_elements(By.CLASS_NAME, "break-words")
            data.append(get_data_from_page(personal_data))
        except selenium.common.exceptions.NoSuchElementException:
            pass
    browser.get(search_url + str(current_page))
with open("data.json", "w") as write_file:
    json.dump(data, write_file)