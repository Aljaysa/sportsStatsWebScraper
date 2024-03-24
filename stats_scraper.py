import requests
import pandas as pd
from bs4 import BeautifulSoup
import inspect
from abc import ABC, abstractmethod 
from enum import Enum

class StatsScraper(ABC):
    _STR_BASEBALL = "Baseball"
    _STR_BASKETBALL = "Basketball"
    
    def __init__(self, mainPageUrl, teamAbreviations, urlExtension, teamCities) -> None:
        self._mainPageUrl = mainPageUrl
        self._teamAbreviations = teamAbreviations
        self._urlExtension = urlExtension
        self._teamCities = teamCities

    def _getUrlTeam(self, teamName):     
        url = ""
        url = url + self._mainPageUrl
        url = url + "/teams"
        url = url + f"/{self._teamAbreviations[teamName]}"
        return url
          
    def _getSoupTeamStats(self, teamName, year):
        url = self._getUrlTeam(teamName)
        url = url + f"/{year}"
        url = url + self._urlExtension 
        return StatsScraper._getSoup(url)

    @staticmethod
    def _getSoup(url):
        r = requests.get(url)
        #print(r)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup

    @abstractmethod
    def _getSoupTeamContracts(self, teamName):
        pass
    
    
    def _getTable(self, soup, tableID):
        table = soup.find("table", id=tableID)
        return table
        
    def _getHeadersFromTable(self, soup, tableID): 
        headers = []
        fullTable = self._getTable(soup, tableID)
        #print(fullTable)
        headersRowWebData = fullTable.find("thead").find().find_all("th") # the extra .find() is to probe into the <tr> html element: <thead> <tr> {All the Header data is here} </tr> </thead> ... so we need to probe into the <tr> as well as the <thead> before we can get to the header data. Then, the .contents is to get all of the headers (<th> and <td> elements) in a list
        for dataCellWebData in headersRowWebData:
            headers.append(dataCellWebData.text)
        return headers
    
    def _getStatsFromTable(self, soup, tableID, posToOmit=[]):
        fullTable = self._getTable(soup, tableID)
        justPlayersStatsTable = fullTable.find("tbody")
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
        for thisPlayer in playersRows:
            thisPlayerStatsNum = []
            thisPlayerStatsWebData = thisPlayer.contents # currently, "th" elements are also included so that the "rank" col in many baseball reference graphs are included for instance. This is because .contents gets all children of a given html element, regardless of what tag it has (<td>, <th>, etc.)
            try: 
                for dataCellWebData in thisPlayerStatsWebData:
                    thisPlayerStatsNum.append(dataCellWebData.text)
            except:
                raise AttributeError("When scraping through a player's stats one col at a time, found that one of this player's stats does not have a text value")
            playersStats.append(thisPlayerStatsNum)
        return playersStats    
    


    
    @staticmethod
    def _raiseErrorInvalidArg(nameOfEnclosingFunc):
        raise ValueError(f"argument provided to function '{nameOfEnclosingFunc}'' invalid")


 
class BaseballStatsScraper(StatsScraper):
    _POS_PLAYER_ABREV = ["C", "1B", "2B", "SS", "3B", "LF", "CF", "RF", "DH", "UT", "OF", "IF", "DH"]
    _PITCHER_ABREV = "P"
    def __init__(self):
        urlStats = "https://www.baseball-reference.com"
        """
        teamCities = [
            "Diamondbacks",
            "Braves",
            "Orioles",
            "Red Sox",
            "Cubs",
            "White Sox",
            "Reds",
            "Guardians",
            "Rockies",
            "Tigers",
            "Marlins",
            "Astros",
            "Royals",
            "Angels",
            "Dodgers",
            "Brewers",
            "Twins",
            "Mets",
            "Yankees",
            "Athletics",
            "Phillies",
            "Pirates",
            "Padres",
            "Giants",
            "Mariners",
            "Cardinals ",
            "Rays",
            "Rangers",
            "Blue Jays",
            "Nationals"
        ]
        """
        teamAbreviations = dict([
            ("Diamondbacks", "ARI"),
            ("Braves", "ATL"),
            ("Orioles", "BAL"),
            ("Red Sox", "BOS"),
            ("Cubs", "CHC"),
            ("White Sox", "CHW"),
            ("Reds", "CIN"),
            ("Guardians", "CLE"),
            ("Rockies", "COL"),
            ("Tigers", "DET"),
            ("Marlins", "MIA"),
            ("Astros", "HOU"),
            ("Royals", "KAN"),
            ("Angels", "LAA"),
            ("Dodgers", "LAD"),
            ("Brewers", "MIL"),
            ("Twins", "MIN"),
            ("Mets", "NYM"),
            ("Yankees", "NYY"),
            ("Athletics", "OAK"),
            ("Phillies", "PHI"),
            ("Pirates", "PIT"),
            ("Padres", "SDP"),
            ("Giants", "SFG"),
            ("Mariners", "SEA"),
            ("Cardinals ", "STL"),
            ("Rays", "TBR"),
            ("Rangers", "TEX"),
            ("Blue Jays", "TOR"),
            ("Nationals", "WSN")
        ])
        urlExtension = ".shtml"
        teamCities = dict([
            ("Diamondbacks", "Arizona"),
            ("Braves", "Atlanta"),
            ("Orioles", "Baltimore"),
            ("Red Sox", "Boston"),
            ("Cubs", "Chicago"),
            ("White Sox", "Chicago"),
            ("Reds", "Cincinnati"),
            ("Guardians", "CLE"),
            ("Rockies", "Colorado"),
            ("Tigers", "Detroit"),
            ("Marlins", "Florida"),
            ("Astros", "Houston"),
            ("Royals", "Kansas City"),
            ("Angels", "Los Angeles"),
            ("Dodgers", "Los Angeles"),
            ("Brewers", "Milwaukee"),
            ("Twins", "Minnesota"),
            ("Mets", "New York"),
            ("Yankees", "New York"),
            ("Athletics", "Oakland"),
            ("Phillies", "Philadelphia"),
            ("Pirates", "Pittsburgh"),
            ("Padres", "San Diego"),
            ("Giants", "San Francisco"),
            ("Mariners", "Seattle"),
            ("Cardinals ", "St. Louis"),
            ("Rays", "Tampa Bay"),
            ("Rangers", "Texas"),
            ("Blue Jays", "Toronto"),
            ("Nationals", "Washington")
        ])
        super().__init__(urlStats, teamAbreviations, urlExtension, teamCities)
        
    def _getSoupTeamContracts(self, teamName):
        url = self._getUrlTeam(teamName)
        url = url + f"/{self._teamCities[teamName].lower()}-{teamName.lower()}-salaries-and-contracts{self._urlExtension}" 
        return self._getSoup(url)
    
    

    def getTeamPitcherHeaders(self, teamName: str, year: str) -> list[str]:
        soup = self._getSoupTeamStats(teamName, year) 
        tableID = "team_pitching"
        return self._getHeadersFromTable(soup, tableID)

    def getTeamPitcherStats(self, teamName: str, year: str) -> list[str]:
        soup = self._getSoupTeamStats(teamName, year)
        tableID = "team_pitching"
        return self._getStatsFromTable(soup, tableID)
    
    def getTeamBatterHeaders(self, teamName: str, year: str) -> list[str]:
        soup = self._getSoupTeamStats(teamName, year)
        tableID = "team_batting" #payroll
        return self._getHeadersFromTable(soup, tableID)
        
    def getTeamBatterStats(self, teamName: str, year: str) -> list[str]:
        soup = self._getSoupTeamStats(teamName, year)
        tableID = "team_batting"
        return self._getStatsFromTable(soup, tableID, ["P"]) 
    
    def getTeamContractHeaders(self, teamName: str) -> list[str]:
        soup = self._getSoupTeamContracts(teamName)
        tableID = "payroll"
        return self._getHeadersFromTable(soup, tableID)
    
    def getTeamContractStats(self, teamName: str) -> list[str]:
        soup = self._getSoupTeamContracts(teamName)
        tableID = "payroll"
        return self._getStatsFromTable(soup, tableID)
    

    
    

class BasketballStatsScraper(StatsScraper):
    def __init__(self):
        urlStats = "https://www.basketball-reference.com"
        teamAbreviations = dict([
            ("Boston", "BOS"),
            ("Philadelphia", "PHI")
        ])
        urlExtension = ".html"
        super().__init__(urlStats, teamAbreviations, urlExtension)

    def getTeamPerGameStats(self, teamName, year):
        tableID = "per_game"
        return self._getStatsFromTable(teamName, year, tableID)
        