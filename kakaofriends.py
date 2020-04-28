from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

path = "C:/Users/Naeun Yoo/Desktop/cps-sec-live/6ths/chromedriver.exe"
driver  = webdriver.Chrome(path)

try:
    driver.get("https://store.kakaofriends.com/kr/index?tab=home")
    time.sleep(1)
    
    searchindex = "죠르디" 
    element = driver.find_element_by_xpath('//*[@id="innerHead"]/div/form/div/input')
    element.send_keys(searchindex) 
    driver.find_element_by_xpath('//*[@id="innerHead"]/div/form/div/button').click()
    time.sleep(5)
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")
    product_block = bs.find("ul", class_= "item-list__Ul-sc-1c138kz-2 ldUgSG").find_all("li", class_= "item__Li-sc-1eldrmh-0 bvdZJN")
    product_info = []

    for p in product_block:
        product_name = p.find("p", class_="item__ItemTitle-sc-1eldrmh-2 gEjWGK").text
        product_price = p.find("p", class_ ='item__Price-sc-1eldrmh-3 gjizjp').text.replace("금액", "")
        print (product_name, ":", product_price)

finally:  
    driver.quit()