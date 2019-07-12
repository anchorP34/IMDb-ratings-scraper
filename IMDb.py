# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 14:37:51 2019

@author: jainanuj7
"""
import requests 
import pandas as pd
from bs4 import BeautifulSoup
from time import strftime 
######################### Change inputs here #########################

# eg for 'The Office' 
# IMDb url: https://www.imdb.com/title/tt0386676/?ref_=ttep_ep_tt
# season_id = 'tt0386676'
season_id = 'tt0386676'

#Total number of seasons
number_of_seasons = 9

#####################################################################

ratings = []
titles = []
votes = []
airdates = []

# Scraper URL
URL = "https://www.imdb.com/title/" + season_id + "/episodes/_ajax"

for season in range(1, number_of_seasons+1):
    print('[', strftime("%H:%M:%S") ,']', 'Finding IMDb ratings for season ', season, '..')
    PARAMS = {'season': season}
    r = requests.get(url = URL, params = PARAMS)
    
    # URL response is in HTML format
    soup = BeautifulSoup(r.content, 'html.parser')
    
    
    rating_divs = soup.findAll("div", {"class": "ipl-rating-widget"})
    for div in rating_divs:
        # Find IMDb rating
        rating_div_inner = div.findAll("div", {"ipl-rating-star small"})
        soup_inner_rating = rating_div_inner[0].findAll("span", {"ipl-rating-star__rating"})
        ratings.append(soup_inner_rating[0].string)
        
        # Find total votes
        soup_inner_votes = rating_div_inner[0].findAll("span", {"ipl-rating-star__total-votes"})
        votes_string = soup_inner_votes[0].string
        votes_string = votes_string.replace(',', '')
        votes_string = votes_string.replace('(', '')
        votes_string = votes_string.replace(')', '')
        votes.append(int(votes_string))
        
    
    # Find episode titles
    title_divs = soup.findAll("strong")
    for div in title_divs:
        titles.append(div.string) 
    #Popping the extra title (eg Season 1, Season 2, etcc) at end for each season (not required)
    titles.pop()
    
    
    # Find airdate
    airdate_divs = soup.findAll("div", {"class": "airdate"})
    for div in airdate_divs:
        airdate_string = div.string
        airdate_string = airdate_string.replace('.', '')
        airdate_string = airdate_string.strip()
        airdates.append(airdate_string)

# Preparing final data    
data = {'Title': titles, 'IMDB Rating': ratings, 'Total Votes': votes, 'Air Date': airdates}
df = pd.DataFrame(data)

# Writing to CSV
df.to_csv(season_id + '.csv', index=False)
print('Finshed!')
