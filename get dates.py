# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 2020
Author: Brandi Beals
Description: Developed for personal use
"""

######################################
# IMPORT PACKAGES
######################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

######################################
# SET WEB DRIVER ENVIRONMENT
######################################

# what's the url and where is your Selenium Chrome driver saved?
url = "https://city.milwaukee.gov/recycle/Curbside-Cart-Collection/Schedule-Set-Out-Information"
driver = webdriver.Chrome('C:/Users/bbeals/Selenium/chromedriver')
driver.implicitly_wait(30)
driver.get(url)

######################################
# SET ADDRESS VARIABLES
######################################

# what's your street address? save it here!
# capitalize the text
address = '4918'
direction = 'W'
street = 'WASHINGTON'
streettype = 'BL'

######################################
# SWITCH TO FORM IFRAME
######################################

# this particular website has an embedded iframe so select that iframe first
iframe = driver.find_element(By.CSS_SELECTOR, 'iframe')
driver.switch_to.frame(iframe)

######################################
# GET FORM ELEMENTS
######################################

# now find the various elements where you need to enter your address
address_element = driver.find_element(By.NAME,'laddr')
direction_element = driver.find_element(By.NAME,'sdir')
street_element = driver.find_element(By.NAME,'sname')
streettype_element = driver.find_element(By.NAME,'stype')

######################################
# ENTER ADDRESS INTO FORM
######################################

# for each element in the form, click it and enter the variable info
# street number first
address_element.click()
address_element.send_keys(address)
# then street direction info
direction_element.click()
direction_element.send_keys(direction)
# then what street you live on
street_element.click()
street_element.send_keys(street)
# then fill in the street type
streettype_element.click()
streettype_element.send_keys(streettype)

######################################
# SUBMIT FORM
######################################

# finally, find and click the Submit button
submit = driver.find_element(By.NAME, 'Submit')
submit.click()

######################################
# SCRAPE RESULTS
######################################

# results should now be on the screen, so let's get 'em!
# save a screenshot (for funsies)
driver.save_screenshot('image.png')
# get the html to parse later
html = driver.page_source
# create soup object
soup = BeautifulSoup(html, 'html.parser')

# save header text to list
category = []
for text in soup.find_all('h2'):
    category.append(text.get_text())

# save bold text to list
date = []
for text in soup.find_all('strong'):
    date.append(text.get_text())

######################################
# FORMAT RESULTS
######################################

# keep 2nd and 4th item in the list
# these correspond to the 1st and 3rd 0-indexed items
# so keep items, stepping by 2
date = date[1:4:2]
df = pd.DataFrame(list(zip(category, date)), 
                  columns = ['Category','Date'])

######################################
# SHUT IT DOWN
######################################

driver.quit()
