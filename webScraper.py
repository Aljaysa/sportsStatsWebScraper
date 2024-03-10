import requests
import pandas as pd
from bs4 import BeautifulSoup
import inspect
from abc import ABC, abstractmethod 

class statsScraper(ABC):
    _STR_BASEBALL = "Baseball"
    _STR_BASKETBALL = "Basketball"
    
    def __init__(self, urlStats, teamAbreviations, urlExtension) -> None:
        self._urlStats = urlStats
        self._teamAbreviations = teamAbreviations
        self._urlExtension = urlExtension
                
    def _getSoupTeamStats(self, city, year):
        url = ""
        url = url + self._urlStats
        url = url + "/teams/"
        url = url + self._teamAbreviations[city]
        url = url + f"/{year}"
        url = url + self._urlExtension 
    
        r = requests.get(url)
        #print(r)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
        
    
    @classmethod
    def _raiseErrorInvalidArg(nameOfEnclosingFunc):
        raise ValueError(f"argument provided to function '{nameOfEnclosingFunc}'' invalid")

class baseballStatsScraper(statsScraper):
    _POS_PLAYER_ABREV = ["C", "1B", "2B", "SS", "3B", "LF", "CF", "RF", "DH", "UT", "OF", "IF", "DH"]
    _PITCHER_ABREV = "P"
    def __init__(self):
        urlStats = "https://www.baseball-reference.com"
        teamAbreviations = dict([
            ("Baltimore", "BAL"),
            ("Texas", "TEX")
        ])
        urlExtension = ".shtml"
        super().__init__(urlStats, teamAbreviations, urlExtension)


    def getBaseballTeamPitcherStats(self, city, year):
        tableID = "team_pitching"
        return self._getBaseballTeamStats(city, year, tableID)
        
    def getBaseballTeamBatterStats(self, city, year):
        tableID = "team_batting"
        return self._getBaseballTeamStats(city, year, tableID, ["P"]) 
         
    def _getBaseballTeamStats(self, city, year, tableID, posToOmit=[]):
        soup = self._getSoupTeamStats(city, year)
        fullStatsTable = soup.find("table", id=tableID)
        justPlayersStatsTable = fullStatsTable.find("tbody")
        playersRows = justPlayersStatsTable.findAll("tr", class_=lambda x : x != "thead")
        #print(playersRows)
        if posToOmit: #if list is not empty
            playersRowsPosOmitted = []
            try:
                for row in playersRows:
                    pos = row.find("td", {'data-stat':'pos'})
                    #print(pos.string)
                    if(pos.string not in posToOmit):
                        playersRowsPosOmitted.append(row) 
                playersRows = playersRowsPosOmitted
            except AttributeError:
                pass
        
        playersStats = []
        for player in playersRows:
            tempPlayer = ()
            name = player.find("td",{'data-stat':'player'})
            tempPlayer = (*tempPlayer, name.text)
            #print(pitcherName.text) 
            age = player.find("td",{'data-stat':'age'})
            tempPlayer = (*tempPlayer, age.text)
            games = player.find("td",{'data-stat':'G'})
            tempPlayer = (*tempPlayer, games.text)
            playersStats.append(tempPlayer)
 
        return playersStats
    
    #def getPlayersRowsPosOmitted()
    

class basketballStatsScraper(statsScraper):
    def __init__(self):
        urlStats = "https://www.basketball-reference.com"
        teamAbreviations = dict(
            ("Boston", "BOS"),
            ("Philadelphia", "PHI")
        )
        urlExtension = ".html"
        super().__init__(urlStats, teamAbreviations, urlExtension)

        