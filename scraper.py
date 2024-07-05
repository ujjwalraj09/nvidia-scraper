from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import re
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.nvidia.com/en-in/geforce/buy/"
driver.get(url)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'general-container')))

soup = BeautifulSoup(driver.page_source, 'lxml')

graphics_cards = {}

sections = soup.find_all('div', class_='general-container')
for section in sections:
    name = None
    price = "N/A"
    
    name_tag = section.find('h3', class_='title')
    if name_tag:
        name = name_tag.get_text(strip=True)
    
    price_tag = section.find('div', class_='startingprice')
    if price_tag:
        price_text = price_tag.get_text(strip=True)
        price_match = re.search(r'[\d,]+', price_text)
        if price_match:
            price = float(price_match.group().replace(',', ''))
    else:
        price_match = re.search(r'Rs\.\s*([\d,]+)', section.get_text())
        if price_match:
            price = float(price_match.group(1).replace(',', ''))
    
    if name:
        graphics_cards[name] = price

driver.quit()

with open("graphics_cards.json", "w", encoding="utf-8") as json_file:
    json.dump(graphics_cards, json_file, ensure_ascii=False, indent=4)

print("Graphic cards and prices have been saved to graphics_cards.json")