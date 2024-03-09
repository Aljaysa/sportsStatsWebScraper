import requests
import pandas as pd
from bs4 import BeautifulSoup
import inspect


"""
statsTableHeaders = statsTable.findAll("th")
headerNames = []
for header in statsTableHeaders:
    headerNames.append(header.text)
#print(headerNames)
"""
class statsScraper:
    __URL_BASEBALL_STATS = "https://www.baseball-reference.com"
    __URL_BASKETBALL_STATS = "https://www.basketball-reference.com"
    __STR_BASEBALL = "Baseball"
    __STR_BASKETBALL = "Basketball"
    
    def __init__(self) -> None:
        pass
    
                
    def __getSoupTeamStats(self, sport, city, year):
        ####todo scrape based on team param
        url = ""
        match sport:
            case statsScraper.__STR_BASEBALL:
                url = url + statsScraper.__URL_BASEBALL_STATS
            case statsScraper.__STR_BASKETBALL:
                url = url + statsScraper.__URL_BASKETBALL_STATS
            case _:
                nameOfEnclosingFunc = inspect.stack()[0][3]
                statsScraper.__raiseErrorInvalidArg(nameOfEnclosingFunc)
        
        url = url + "/teams/"
        
        match city:
            case "Baltimore":
                url = url + "BAL"
            case "Texas":
                url = url + "TEX"
            case _:
                nameOfEnclosingFunc = inspect.stack()[0][3]
                statsScraper.__raiseErrorInvalidArg(nameOfEnclosingFunc)
                
        url = url + f"/{year}"
            
        match sport:
            case statsScraper.__STR_BASEBALL:
                url = url + ".shtml"
            case statsScraper.__STR_BASKETBALL:
                url = url + ".html"
            case _:
                nameOfEnclosingFunc = inspect.stack()[0][3]
                statsScraper.__raiseErrorInvalidArg(nameOfEnclosingFunc)    
            
        r = requests.get(url)
        #print(r)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    
    def getBaseballTeamPitcherStats(self, city, year):
        soup = self.__getSoupTeamStats(statsScraper.__STR_BASEBALL, city, year)
        statsTable = soup.find("table", id="team_batting")
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
        return pitchersStats

    @classmethod
    def __raiseErrorInvalidArg(nameOfEnclosingFunc):
        raise ValueError(f'argument provided to function "{nameOfEnclosingFunc}" invalid')
