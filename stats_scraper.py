import requests
from bs4 import BeautifulSoup
import inspect
from abc import ABC, abstractmethod 
from enum import Enum
import sys
import re

class StatsScraper(ABC):
    """A class to gets the stats and data of a sports stat website into data types like lists
    _STR_BASEBALL (str): the word Baseball in string format
    _STR_BASKETBALL (str): the word Basketball in string format
    Methods:
    removeAllBlankRows(table): Takes a table and returns the same table but with rows that only contain '' values removed
    """         
    _STR_BASEBALL = "Baseball"
    _STR_BASKETBALL = "Basketball"
    
    def __init__(self, mainPageUrl, teamAbreviations, urlExtension, teamCities) -> None:
        """
        Args:
            mainPageUrl (str): base url of the main page of the sports stats website. All subpages' URLs add onto this URL ie: baseURL -> baseURL/moreURLWords/moreURLWords
            teamAbreviations (dict): a dictionary of (str, str) (key, value) pairs where the key is the team's name (ie. "Red Sox" for Boston) and the value is the 3 letter abreviation that a given sports stats website uses to identify every team (ie. baseball-reference.com uses the 3 letters "BAL" to represent Baltimore Orioles)
            urlExtension (str): the extension (ie. .html, .shtml, .com, etc.) that ends every URL of a any of the pages of a given sports stats website (ie. every URL on baseball-reference.com ends with .shtml)
            teamCities (dict): a dictionary of (str, str) (key, value) pairs where the key is the team's name (ie. "Red Sox" for Boston) and the value is the city of that team (ie. "Toronto" for Blue Jays)
        """        
        self._mainPageUrl = mainPageUrl
        self._teamAbreviations = teamAbreviations
        self._urlExtension = urlExtension
        self._teamCities = teamCities

    def _getUrlTeam(self, teamName): 
        """Gets the Baseball Reference URL of a team's general stats page (this page is not specific to a certain season)
        Args:
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
        Returns:
            str: the Baseball Reference URL of a team's general stats page (this page is not specific to a certain season)
        """            
        url = ""
        url = url + self._mainPageUrl
        url = url + "/teams"
        url = url + f"/{self._teamAbreviations[teamName]}"
        return url
          
    def _getSoupTeamStats(self, teamName, year):
        """Gets the BeautifulSoup object that contains the tree to be traversed of html web elements for a team's stats page
        Args:
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
            year (str or int): year of the season to get the stats for
        Returns:
            BeautifulSoup: tree to be traversed of html web elements for a team's stats page
        """        
        url = self._getUrlTeam(teamName)
        url = url + f"/{year}"
        url = url + self._urlExtension 
        return StatsScraper._getSoup(url)

    @staticmethod
    def _getSoup(url):
        """Gets the BeautifulSoup object that contains the tree to be traversed of html web elements of any webpage
        Args:
            url (str): url of the webpage to get the html data from
        Returns:
            BeautifulSoup: tree to be traversed of html web elements
        """        
        r = requests.get(url)
        #print(r)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    
    def _getTable(self, soup, tableID):
        """Gets the a desired table on a webpage
        Args:
            soup (BeautifulSoup): the parent html web element where we look into it's children and descendants (children of those children and so on) for the table
            tableID (str): the value of the "id" attribute of the table html web element
        Returns:
            BeautifulSoup: the desired table that like it's parent, is also a tree of html elements/BeautifulSoup objects
        """        
        #table = soup.find("body").find("div", id="wrap").find("div", id="content")#.find("div", id="players_standard_batting").find("div", id="table_container is_setup").find("table", id="players_standard_batting")
        table = soup.find("table", id=tableID)
        if(table is None):
            blockedBySiteMsg = soup.find("body").find("div", id="wrap").find("div", id="content")
            #print(blockedBySiteMsg)
            raise TableNotFoundException(blockedBySiteMsg)
        #print(table)
        return table
        
     
        
    def _getHeadersFromTable(self, soup, tableID): 
        """Gets a list of headers of a table on a webpage
        Args:
            soup (BeautifulSoup): the parent html web element where we look into it's children and descendants (children of those children and so on) for the table
            tableID (str): the value of the "id" attribute of the table html web element
        Returns:
            list: a list of strings representing the header columns of the table
        """ 
        headers = []
        #with open("output.txt", "a") as f:
        #    f.write(soup)
        #out=sys.stdout
        #out.write(soup.prettify())
        fullTable = self._getTable(soup, tableID)
        #print(fullTable) #uncomment this line to see the html for the table
        def stat_selector(tag):
            return tag.name == "th" or tag.name == "td"
        headersRowWebData = fullTable.find("thead").find().find_all(stat_selector) # the extra .find() is to probe into the <tr> html element: <thead> <tr> {All the Header data is here} </tr> </thead> ... so we need to probe into the <tr> as well as the <thead> before we can get to the header data. Then, the .contents is to get all of the headers (<th> and <td> elements) in a list
        for dataCellWebData in headersRowWebData:
            headers.append(dataCellWebData.text) #surround this in try block later because maybe element doesn't have .text attribute?
        return headers
    
    def _getStatsFromTable(self, soup, tableID, posToOmit=[]):
        """Gets a list  of stats from a table from a webpage
        Args:
            soup (BeautifulSoup): the parent html web element where we look into it's children and descendants (children of those children and so on) for the table
            tableID (str): the value of the "id" attribute of the table html web element
            posToOmit (list, optional): a list of the positions where all players with one of these positions will be ommitted from the returned list. Defaults to [].
        Returns:
            list: a list (2D if there are multiple rows not including the header row) of stats (strings) from the table
        """        
        fullTable = self._getTable(soup, tableID)
        justPlayersStatsTable = fullTable.find("tbody")
        playersRows = justPlayersStatsTable.findAll("tr", class_=lambda x : x != "thead") #"tr", class_=lambda x : x != "thead"
        #print(playersRows)
        # if posToOmit: #if list is not empty #currently commented out as it overcomplicated things but the purpose of this block is to have pitches ommitted from the batters stats
            # playersRowsPosOmitted = []
            # try: #try block is to provide the same list of player rows as before but with all players with a given position removed
            #     for row in playersRows:
            #         pos = row.find("td", {'data-stat':'pos'})
            #         #print(pos.string)
            #         if(pos.string not in posToOmit):
            #             playersRowsPosOmitted.append(row) 
            #     playersRows = playersRowsPosOmitted
            # except AttributeError: #if row doesn't have a 'pos' attribute so can't even check its value to check position
            #     pass 
        playersStats = []
        for thisPlayer in playersRows: #now that we have all player's BeautifulSoup objs in a list, extract the stats
            def stat_selector(tag):
                return tag.name == "th" or tag.name == "td"
            thisPlayerStatsWebData = thisPlayer.find_all(stat_selector) # .contents instead of find_all("td")  gets all <td> elements and "th" elements are also included so that the "rank" col in many baseball reference graphs are included for instance. This is because .contents gets all children of a given html element, regardless of what tag it has (<td>, <th>, etc.). We don't want this however as .contents was returning " " blank elements for some reason
            #print(thisPlayerStatsWebData)
            thisPlayerStatsNum = StatsScraper._getStatsInRow(thisPlayerStatsWebData)
            if(len(thisPlayerStatsNum) != 0):
                playersStats.append(thisPlayerStatsNum)
        return playersStats      

    
    @staticmethod
    def _raiseErrorInvalidArg(nameOfEnclosingFunc):
        """Raises an Exception with a message. Used for situations when an argument provided to a funciton is invalid (not one of the options supported)
        Args:
            nameOfEnclosingFunc (str): name of the function that the exception is thrown
        Raises:
            ValueError: exception object to be raised
        """        
        raise ValueError(f"argument provided to function '{nameOfEnclosingFunc}'' invalid")

    @staticmethod
    def _getStatsInRow(thisPlayerStatsWebData):
        """Gets the stats of a given player/row of a table on a webpage
        Args:
            thisPlayerStatsWebData (BeautifulSoup): the html web element data for a given player/row of a table
        Raises:
            AttributeError: If when scraping through a player's stats one col at a time, it is found that one of this player's stats does not have a text value
        Returns:
            list: a list of strings representing the stats of a player/row of a table
        """        
        thisPlayerStatsNum = []
        try: 
            for dataCellWebData in thisPlayerStatsWebData:
                thisPlayerStatsNum.append(dataCellWebData.text)
                #### The following try block is here so that summary type rows that have one value span multiple rows (see image): [] won't be added to the list of stats
                try: # to get stats list to the correct len even though some values in the table span multiple columns
                    intColSpan = int(dataCellWebData["colspan"]) 
                    if(intColSpan > 1):
                        return []
                        #for _ in range(intColSpan - 1): # This option can be used instead of the line above if instead of not adding the row to the list of stats, you do want to add the row but you just want to add blank values ("") for all the cols that the value spans for (so that the num of cols in this row matches the num of cols in every other row)
                        #    thisPlayerStatsNum.append("")
                except:
                    pass
                #### End of try block 
        except:
            raise AttributeError("When scraping through a player's stats one col at a time, found that one of this player's stats does not have a text value") # toDo could turn this into logging so that dummy val of '' is inserted and no exception thrown but the issue is logged
        return thisPlayerStatsNum
    
    @staticmethod
    def removeAllBlankRows(table):
        """Takes a table and returns the same table but with rows that only contain '' values removed
        Args:
            table (list): 2D list of strings that may or may not have blank rows
        Returns:
            list: 2D list of strings with rows that only contain '' values removed
        """        
        tableBlankRowsRemoved = []
        for row in table:
            isRowBlank = True
            for col in row:
                if(col != ''):
                    isRowBlank = False
            if(not isRowBlank):
                tableBlankRowsRemoved.append(row)
        return tableBlankRowsRemoved



 
class BaseballStatsScraper(StatsScraper):
    """A class to gets the stats and data of a baseball stat website into data types like lists
    _POS_PLAYER_ABREV:  One letter abbriviation representing all other positions than pitcher 
    _PITCHER_ABREV: One letter abbriviation representing pitcher position
        Methods:
        getTeamPitcherHeaders: Gets a list of headers of the pitcher basic stats table on a team's main stats page
        getTeamPitcherStats: Gets a list of stats of the pitcher basic stats table on a team's main stats page
        getTeamBatterHeaders: Gets a list of headers of the batter basic stats table on a team's main stats page
        getTeamBatterStats: Gets a list of stats of the batter basic stats table on a team's main stats page
        getTeamContractHeaders: Gets a list of headers of the contracts table on a team's contract stats page
        getTeamContractStats: Gets a list of stats of the contracts table on a team's contract stats page
    """
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
            ("Guardians", "Cleveland"),
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
        """Gets the BeautifulSoup object that contains the tree to be traversed of html web elements for a team's contract stats page
        Args:
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
        Returns:
           BeautifulSoup: tree to be traversed of html web elements for a team's contract stats page
        """        
        
        url = self._getUrlTeam(teamName)
        url = url + f"/{(self._teamCities[teamName].replace(' ', '-')).lower()}-{(teamName.replace(' ', '-')).lower()}-salaries-and-contracts{self._urlExtension}" 
        soup = self._getSoup(url)
        return soup

    def getTeamPitcherHeaders(self, teamName: str, year: str) -> list[str]:
        """Gets a list of headers of the pitcher basic stats table on a team's main stats page
        Args:
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
            year (str or int): year of the season to get the stats for
        Returns:
            list: a list of strings representing the header columns of the table
        """ 
        soup = self._getSoupTeamStats(teamName, year) 
        tableID = "team_pitching"
        return self._getHeadersFromTable(soup, tableID)

    def getTeamPitcherStats(self, teamName: str, year: str) -> list[str]:
        """Gets a list of stats of the pitcher basic stats table on a team's main stats page
        Args:
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
            year (str or int): year of the season to get the stats for
        Returns:
            list: a list (2D if there are multiple rows not including the header row) of stats (strings) from the table
        """ 
        soup = self._getSoupTeamStats(teamName, year)
        tableID = "team_pitching"
        return self._getStatsFromTable(soup, tableID)
    
    def getTeamBatterHeaders(self, teamName: str, year: str) -> list[str]:
        """Gets a list of headers of the batter basic stats table on a team's main stats page
        Args:
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
            year (str or int): year of the season to get the stats for
        Returns:
            list: a list of strings representing the header columns of the table
        """ 
        soup = self._getSoupTeamStats(teamName, year)
        tableID = "players_standard_batting" #payroll
        return self._getHeadersFromTable(soup, tableID)
        
    def getTeamBatterStats(self, teamName: str, year: str) -> list[str]:
        """Gets a list of stats of the batter basic stats table on a team's main stats page
        Args:
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
            year (str or int): year of the season to get the stats for
        Returns:
            list: a list (2D if there are multiple rows not including the header row) of stats (strings) from the table
        """ 
        soup = self._getSoupTeamStats(teamName, year)
        tableID = "players_standard_batting"
        return self._getStatsFromTable(soup, tableID, ["P"]) 
    
    def getTeamContractHeaders(self, teamName: str) -> list[str]:
        """Gets a list of headers of the contracts table on a team's contract stats page
        Args:
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
        Returns:
            list: a list of strings representing the header columns of the table
        """
        soup = self._getSoupTeamContracts(teamName)
        tableID = "payroll"
        return self._getHeadersFromTable(soup, tableID)
    
    def getTeamContractStats(self, teamName: str) -> list[str]:
        """Gets a list of stats of the contracts table on a team's contract stats page
        Args:
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
        Returns:
            list: a list (2D if there are multiple rows not including the header row) of stats (strings) from the table
        """ 
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
        """Gets a list of stats of the "per game" table on a team's main stats page
        Args:
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
            year (str or int): year of the season to get the stats for
        Returns:
            list: a list (2D if there are multiple rows not including the header row) of stats (strings) from the table
        """ 
        tableID = "per_game"
        return self._getStatsFromTable(teamName, year, tableID)
        
class TableNotFoundException(Exception):
    def __init__(self, message, errors=None):            
        # Call the base class constructor with the parameters it needs
        super().__init__("Table while scraping HTML file was not found, possibly due to the ID of the table given being being incorrect, or the website blocking webscrapers/bots, etc. This is the data that was returned after tried to get your desired table: " + message)
        # Now for your custom code...
        self.errors = errors