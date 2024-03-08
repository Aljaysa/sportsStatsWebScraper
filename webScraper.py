import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.baseball-reference.com/teams/BAL/2023.shtml"
r = requests.get(url)
print(r)

soup = BeautifulSoup(r.text, "html.parser")

statsTable = soup.find("table", id="team_batting")

statsTableHeaders = statsTable.findAll("th")
headerNames = []
for header in statsTableHeaders:
    headerNames.append(header.text)
#print(headerNames)

pitchersRows = []  
statsTableRows = statsTable.findAll("tr")
for row in statsTableRows[1:]:
    try:
        pos = row.find("td")
        #print(pos.string)
        if(pos.string == "P"):
            pitchersRows.append(row)
    except AttributeError:
        pass
  
pitchersStats = []
  
for pitcher in pitchersRows:
    tempPitcher = ()
    name = pitcher.find("td",{'data-stat':'player'})
    tempPitcher = (*tempPitcher, name.text)
    #print(pitcherName.text) 
    age = pitcher.find("td",{'data-stat':'age'})
    tempPitcher = (*tempPitcher, age.text)
    games = pitcher.find("td",{'data-stat':'G'})
    tempPitcher = (*tempPitcher, games.text)
    pitchersStats.append(tempPitcher)
"""
for pitcher in pitchersStats:
    print(pitcher)
"""


