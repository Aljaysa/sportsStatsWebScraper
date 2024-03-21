import requests
import pandas as pd
from bs4 import BeautifulSoup
import inspect
from abc import ABC, abstractmethod 
import ast, re
from enum import Enum

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
    
    def _getTable(self, city, year, tableID):
        soup = self._getSoupTeamStats(city, year)
        table = soup.find("table", id=tableID)
        return table
        
    def _getHeadersFromTable(self, city, year, tableID):  
        headers = []  
        fullTable = self._getTable(city, year, tableID)
        headersRowWebData = fullTable.find("thead").find().find_all("th") # the extra .find() is to probe into the <tr> html element: <thead> <tr> {All the Header data is here} </tr> </thead> ... so we need to probe into the <tr> as well as the <thead> before we can get to the header data. Then, the .contents is to get all of the headers (<th> and <td> elements) in a list
        #print(headersRowWebData)
        for dataCellWebData in headersRowWebData:
            headers.append(dataCellWebData.text)
        return headers
    
    def _getStatsFromTable(self, city, year, tableID, posToOmit=[]):
        fullTable = self._getTable(city, year, tableID)
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
    def returnInferredType(toInfer):
        if len(toInfer) == 0: return None
        try:
            #print(type(ast.literal_eval(toInfer)))
            return type(ast.literal_eval(toInfer))
        except ValueError:
            return type(" ")
        except SyntaxError:
            return type(" ")
    
    @staticmethod
    def getInferredTypesFromStrings(strList):
        typeList = [] 
        for str in strList:
            typeList.append(statsScraper.returnInferredType(str))
            #print(f"{str}: {statsScraper.returnInferredType(str)}")
        #print(typeList)
        return typeList

    
    @staticmethod
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
        urlExtension = ".shtml" #.shtml
        super().__init__(urlStats, teamAbreviations, urlExtension)

    def getTeamPitcherHeaders(self, city, year):
        tableID = "team_pitching"
        return self._getHeadersFromTable(city, year, tableID)

    def getTeamPitcherStats(self, city, year):
        tableID = "team_pitching"
        return self._getStatsFromTable(city, year, tableID)
    
    def getTeamBatterHeaders(self, city, year):
        tableID = "team_batting" #payroll
        return self._getHeadersFromTable(city, year, tableID)
        
    def getTeamBatterStats(self, city, year):
        tableID = "team_batting"
        return self._getStatsFromTable(city, year, tableID, ["P"]) 
        
    
    

class basketballStatsScraper(statsScraper):
    def __init__(self):
        urlStats = "https://www.basketball-reference.com"
        teamAbreviations = dict([
            ("Boston", "BOS"),
            ("Philadelphia", "PHI")
        ])
        urlExtension = ".html"
        super().__init__(urlStats, teamAbreviations, urlExtension)

    def getTeamPerGameStats(self, city, year):
        tableID = "per_game"
        return self._getStatsFromTable(city, year, tableID)
        