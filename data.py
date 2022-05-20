# -*- coding: utf-8 -*-
"""

@author: Vimal Raj
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

driver = webdriver.Chrome("C:/Users/OFFICE1/Downloads/chromedriver_win32/chromedriver.exe")


genres = [] # list to store genres

maingames={} #List to store name of the game
maincount={} #List to store count of the game
mainratings={} #List to store rating of the game
games=[]
count=[]
ratings=[]
data_frame=[]
driver.get("https://www.crazygames.com/c/action")

content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

superlinks = soup.find_all('div', class_="MuiGrid-root MuiGrid-item css-1wxaqej")
for s in superlinks[1:11]:
    games=[]
    count=[]
    ratings=[]
    
    mainlink = s.find('a', href=True)
    connect = mainlink['href']
    genre = connect.split('https://www.crazygames.com/c/')[1]
    genres.append(genre)

    mainpage = requests.get(connect)
    mainsoup = BeautifulSoup(mainpage.content, "html.parser")
    
    for a in mainsoup.find_all('div', class_=["MuiGrid-root", "MuiGrid-container", "MuiGrid-spacing-xs-undefined", "css-cp1wkv"]):

        links = a.find_all('a', class_="css-1p3cwhb", href=True)
        for link in links:
            sublink = link['href']
            page = requests.get(sublink)
            subsoup = BeautifulSoup(page.content, "html.parser")

            gamelist = subsoup.find_all('h1', class_=["MuiTypography-root", "MuiTypography-h1", "css-1khpzc0"])
            for x in gamelist:
                games.append(x.text)

            countlist = subsoup.find_all('div', class_="css-1b86dh0")
            for b in countlist:
                count.append(b.text)

            ratinglist = subsoup.find_all('div', class_="MuiGrid-root MuiGrid-item css-1fn27vw")
            for y in ratinglist:
                ratings.append(y.text)

    # maingames[genre] = games
    # mainratings[genre] = ratings
    # maincount[genre] = count
    data_frame.append(pd.DataFrame({'Game': games, 'Count': count, 'Ratings': ratings}))
    

with pd.ExcelWriter("games.xlsx") as writer:
    for i in range(len(genres)):
        data_frame[i].to_excel(writer, sheet_name=genres[i], index=False)

driver.close()


