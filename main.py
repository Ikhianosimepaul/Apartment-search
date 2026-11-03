import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.webdriver.common.by import By
import requests
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(chrome_options)

headers = {
    "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36",
    "ACCEPT-LANGUAGE": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=headers)
zillow_web_page = response.text

soup = BeautifulSoup(zillow_web_page, "html.parser")
links = [link.get("href") for link in soup.find_all(name="a", class_="property-card-link")]
prices = [price.getText().split("+")[0].split("/")[0] for price in soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")]
address = [re.sub(r"\s+", " ", re.sub(r"[\r\n|]+", " ", add.getText())).strip()
           for add in soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")]

for n in range(len(links)):
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfEurO83esB6NDsjAhA1PyL7WJAxI6yOekGie5_U7Sy9-Oycw/viewform")
    time.sleep(2)

    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    try:
        address_input.send_keys(address[n])
        price_input.send_keys(prices[n])
        link_input.send_keys(links[n])
        submit_button.click()
    except NoSuchElementException:
        time.sleep(5)



