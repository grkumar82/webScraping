'''
This is a simple webscraper program that extracts information from below website.
It queries the website, creates a data fram and loads the data in a CSV format.
Source: https://www.adamchoi.co.uk/teamgoals/detailed
Lesson: https://www.youtube.com/watch?v=UOsRrxMKJYk
Refoctored the code to suit the latest Selenium release
'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time


s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
# website for scraping data
website = 'https://www.adamchoi.co.uk/teamgoals/detailed'
# open Google Chrome with chromedriver
driver.get(website)
# locate a button to get all matches info
all_matches_button = driver.find_element("xpath", "//label[@analytics-event='All matches']")
# click on a button
all_matches_button.click()

# select a particular country from the drop-down provided
drop_down = Select(driver.find_element(By.ID, 'country'))
drop_down.select_by_visible_text('Spain')

# wait for sixty seconds for the page to load
time.sleep(60)

# matches information
matches = driver.find_elements(By.TAG_NAME, 'tr')

# lists to capture the four fields from the table
# date of the match
date = []
# home_team
home_team = []
# final score
score = []
# opposing team
away_team = []

# loop through the matches
for match in matches:
    date.append(match.find_element(By.XPATH, "//td[1]").text)
    home_team.append(match.find_element(By.XPATH, "//td[2]").text)
    score.append(match.find_element(By.XPATH, "//td[3]").text)
    away_team.append(match.find_element(By.XPATH, "//td[4]").text)

# check
# print(date, home_team, score, away_team)

# close the driver
driver.quit()

# create dataframe to store elements prior to pushing to CSV file
df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
df.to_csv('soccer_data.csv', index=True)
