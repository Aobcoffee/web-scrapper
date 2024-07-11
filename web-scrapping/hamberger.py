from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
import requests
from bs4 import BeautifulSoup
import time
import json
import account
import hamberger_list


def wait_locator(driver, locator, key):
    try:
        wait = WebDriverWait(driver, 50)
        element = wait.until(EC.presence_of_element_located(locator))
        
        element.send_keys(key)
    
    except NoSuchElementException:
        print(f"Error: Could not find element using the locator: {locator}")
        
    except StaleElementReferenceException:
        print("Error: The element reference has gone stale. Trying to relocate the element.")
        
        # Relocate the element
        element = driver.find_element(*locator)
        element.send_keys(key)


def driver_setup(driver):

    driver.get(account.hamberger_login_url) 

    # login page
    driver.find_element(By.ID, "loginname").send_keys(account.hamberger["loginname"])
    driver.find_element(By.ID, "passwort_login").send_keys(account.hamberger["passwort"])

    login_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-block.btn-login[type='submit'][id='btnSubmit']")
    driver.execute_script("arguments[0].click();", login_button)
    time.sleep(1)


def collect_data(article_list: list):

    all_data = []

    for num in article_list:
        search_box = (By.CSS_SELECTOR, "#search-term")
        wait_locator(driver, search_box, num)
        time.sleep(2)
        
        driver.find_element(By.CSS_SELECTOR, "#search-term").send_keys(Keys.ENTER)
        time.sleep(2)


        soup = BeautifulSoup(driver.page_source, "lxml")
        container = soup.find("tr", {"class": "ui-table-rows-even"})

        try:
            name = container.find_all("td")[3]
            price_wrappers = container.find_all("span", class_="price-wrapper")
            price=[price.text.split(" ")[0] for price in price_wrappers]
            
            
            data = {
                "article_number" : name.text.split(" ")[0],
                "name" : " ".join(name.text.split(" ")[1:]),
                "price" : price
            }         
        except:
            data = {
                "article_number" : num,
                "name" : "",
                "price" : ""
            }  


        all_data.append(data)

        # clear input box
        driver.find_element(By.CSS_SELECTOR, "#search-term").clear()
        time.sleep(1)

    return all_data



if __name__ == "__main__":

    # setup driver
  
    driver = webdriver.Chrome(service=ChromeService( 
        ChromeDriverManager().install())) 
    actions = ActionChains(driver)

    driver_setup(driver=driver)
    

    # cart page
    driver.get(account.hamberger_cart_url) 
    all_data = collect_data(article_list=hamberger_list.article_list)

    # save json file
    with open(f'json/hamberger3.json', 'w') as f:
        json.dump(all_data, f, indent=4)
        print(f"Successfully saved data to json/hamberger3.json") 
