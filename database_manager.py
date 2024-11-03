import sqlite3

import stats_database_utility
from stats_scraper import StatsScraper as StatsScraper
from stats_scraper import BaseballStatsScraper as BaseballStatsScraper
from stats_scraper import BasketballStatsScraper as BasketballStatsScraper



class DatabaseManager:
    """A class to coordinate the scraping of data from sports stats websites and the uploading and management of those stats in an SQL database
    """
     
    
    def __init__(self, databaseFileName):
        self.baseballStatsScraper = BaseballStatsScraper()
        self.databaseFileName = databaseFileName

    def getTableNameBasicBatterStats(self, teamName, year):
        teamNameWithoutSpaces = teamName.replace(" ", "")
        tableName = f"{teamNameWithoutSpaces}{year}BasicBatterStats"
        return tableName

    def uploadTeamBasicBatterStats(self, teamName, year):   
        """Adds every player from a baseball team's basic batter stats on its team's main page to a database
        Args:
            database (sqlite3.Connection): database to upload to
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
            year (str or int): year of the season to get the stats for
        """      
        with sqlite3.connect(self.databaseFileName) as database:  
            tableName = self.getTableNameBasicBatterStats(teamName, year)
            headers = stats_database_utility.formatTableHeaders(self.baseballStatsScraper.getTeamBatterHeaders(teamName, year))
            stats = self.baseballStatsScraper.getTeamBatterStats(teamName, year)
            #stats removeAllBlankRows
            headerTypes = stats_database_utility.getInferredTypesFromStrings(stats[0])
            createTableCmd = stats_database_utility.getCreateTableCmd(tableName, headers, headerTypes)
            try:
                database.execute(stats_database_utility.getDropTableCmd(tableName))
            except sqlite3.OperationalError: #don't delete table if it doesn't exist
                pass
            database.execute(createTableCmd)
            insertIntoTableCmd = stats_database_utility.getInsertIntoCmd(tableName, headers)
            for statRow in stats:
                database.execute(insertIntoTableCmd, statRow)
            database.commit()
            
    def uploadTeamContracts(self, teamName):   
        with sqlite3.connect(self.databaseFileName) as database:  
            tableName = f"{teamName.capitalize()}Contracts"
            headers = stats_database_utility.formatTableHeaders(self.baseballStatsScraper.getTeamContractHeaders(teamName))
            stats = self.baseballStatsScraper.getTeamContractStats(teamName)
            headerTypes = stats_database_utility.getInferredTypesFromStrings(stats[0])
            createTableCmd = stats_database_utility.getCreateTableCmd(tableName, headers, headerTypes)
            try:
                database.execute(stats_database_utility.getDropTableCmd(tableName))
            except sqlite3.OperationalError: #don't delete table if it doesn't exist
                pass
            database.execute(createTableCmd)
            insertIntoTableCmd = stats_database_utility.getInsertIntoCmd(tableName, headers)
            for statRow in stats:
                #print(statRow)
                database.execute(insertIntoTableCmd, statRow)
            database.commit()
            
    def uploadAllTeamsContracts(self):
        for teamName in self.baseballStatsScraper._teamCities:
            try:
                self.uploadTeamContracts(teamName)
            except Exception as e:
                print(f"{teamName}: {e}")
                
    def uploadAllTeamsBasicBatterStats(self, year):
        for teamName in self.baseballStatsScraper._teamCities:
            try:
                self.uploadTeamBasicBatterStats(teamName, year)
            except Exception as e:
                print(f"{teamName}: {e}")
    
    def selectAllBasicBatterStats(self, teamName, year):
        return self.selectBasicBatterStats(self, teamName, year, "*")
    
    def selectBasicBatterStats(self, teamName, year, headers: list):
        with sqlite3.connect(self.databaseFileName) as database:
            tableName = self.getTableNameBasicBatterStats(teamName, year)
            selectCmd = stats_database_utility.getSelectCmd(tableName, headers)
            #print(selectCmd)
            allDatabaseEntries = database.execute(selectCmd)
            database.commit()
            #NOTE: if you add any database.execute commands after this point, don't forget to add line database.commit()
            databaseData = allDatabaseEntries.fetchall()
            if(len(headers) == 1):
                databaseDataSingleVals = []
                for (tupleVal) in databaseData:
                    #print(tupleVal[0])
                    databaseDataSingleVals.append(tupleVal[0]) 
                return databaseDataSingleVals    
            else:   
                return(databaseData)
        
    



   
   
