import sqlite3

from stats_database_utility import StatsDatabaseUtility as StatsDatabaseUtility
from stats_scraper import StatsScraper as StatsScraper
from stats_scraper import BaseballStatsScraper as BaseballStatsScraper
from stats_scraper import BasketballStatsScraper as BasketballStatsScraper
from stats_visualizer import StatsVisualizer

class DatabaseStatsScraperManager():
    """A class to coordinate the scraping of data from sports stats websites and the uploading and management of those stats in an SQL database
    """
    statsVisSavePath = 'website\embeddedHTML\statsGraphs\\'  
    
    def __init__(self):
        self.baseballStatsScraper = BaseballStatsScraper()

    def getTableNameBasicBatterStats(self, teamName, year):
        teamNameWithoutSpaces = teamName.replace(" ", "")
        tableName = f"{teamNameWithoutSpaces}{year}BasicBatterStats"
        return tableName

    def uploadTeamBasicBatterStats(self, database, teamName, year):   
        """Adds every player from a baseball team's basic batter stats on its team's main page to a database
        Args:
            database (sqlite3.Connection): database to upload to
            teamName (str): name of the sports team (ie. "Red Sox" for Boston)
            year (str or int): year of the season to get the stats for
        """        
        tableName = self.getTableNameBasicBatterStats(teamName, year)
        headers = StatsDatabaseUtility.formatTableHeaders(self.baseballStatsScraper.getTeamBatterHeaders(teamName, year))
        stats = self.baseballStatsScraper.getTeamBatterStats(teamName, year)
        #stats removeAllBlankRows
        headerTypes = StatsDatabaseUtility.getInferredTypesFromStrings(stats[0])
        createTableCmd = StatsDatabaseUtility.getCreateTableCmd(tableName, headers, headerTypes)
        try:
            database.execute(StatsDatabaseUtility.getDropTableCmd(tableName))
        except sqlite3.OperationalError: #don't delete table if it doesn't exist
            pass
        database.execute(createTableCmd)
        insertIntoTableCmd = StatsDatabaseUtility.getInsertIntoCmd(tableName, headers)
        for statRow in stats:
            database.execute(insertIntoTableCmd, statRow)
            
    def uploadTeamContracts(self, database, teamName):   
        tableName = f"{teamName.capitalize()}Contracts"
        headers = StatsDatabaseUtility.formatTableHeaders(self.baseballStatsScraper.getTeamContractHeaders(teamName))
        stats = self.baseballStatsScraper.getTeamContractStats(teamName)
        headerTypes = StatsDatabaseUtility.getInferredTypesFromStrings(stats[0])
        createTableCmd = StatsDatabaseUtility.getCreateTableCmd(tableName, headers, headerTypes)
        try:
            database.execute(StatsDatabaseUtility.getDropTableCmd(tableName))
        except sqlite3.OperationalError: #don't delete table if it doesn't exist
            pass
        database.execute(createTableCmd)
        insertIntoTableCmd = StatsDatabaseUtility.getInsertIntoCmd(tableName, headers)
        for statRow in stats:
            #print(statRow)
            database.execute(insertIntoTableCmd, statRow)
            
    def uploadAllTeamsContracts(self, database):
        for teamName in self.baseballStatsScraper._teamCities:
            try:
                self.uploadTeamContracts(database, teamName)
            except Exception as e:
                print(f"{teamName}: {e}")
                
    def uploadAllTeamsBasicBatterStats(self, database, year):
        for teamName in self.baseballStatsScraper._teamCities:
            try:
                self.uploadTeamBasicBatterStats(database, teamName, year)
            except Exception as e:
                print(f"{teamName}: {e}")
    
    def selectAllBasicBatterStats(self, database, teamName, year):
        return self.selectBasicBatterStats(self, database, teamName, year, "*")
    
    def selectBasicBatterStats(self, database, teamName, year, headers: list):
        tableName = self.getTableNameBasicBatterStats(teamName, year)
        selectCmd = StatsDatabaseUtility.getSelectCmd(tableName, headers)
        #print(selectCmd)
        allDatabaseEntries = database.execute(selectCmd)
        databaseData = allDatabaseEntries.fetchall()
        if(len(headers) == 1):
            databaseDataSingleVals = []
            for (tupleVal) in databaseData:
                #print(tupleVal[0])
                databaseDataSingleVals.append(tupleVal[0]) 
            return databaseDataSingleVals    
        else:     
            return(databaseData)
    
    @staticmethod
    def convertStringsToFloats(strList):
        floatList = []
        for stringVal in strList:
            try:
                floatList.append(float(stringVal))
            except ValueError:
                floatList.append(float(0))
        return floatList
            
       
    def makeBasicBatterStatsScatterplotHTML(self, teamName, year, xHeaderName, yHeaderName):
        yData = self.selectBasicBatterStats(statsDb, teamName, year, [yHeaderName])
        xData = self.selectBasicBatterStats(statsDb, teamName, year, [xHeaderName])
        names = self.selectBasicBatterStats(statsDb, teamName, year, ["Name"])
        teamNameWithoutSpaces = teamName.replace(" ", "")
        htmlFileName = f"{DatabaseStatsScraperManager.statsVisSavePath}{teamNameWithoutSpaces}{year}{xHeaderName}Vs{yHeaderName}.html"
        graphTitle = f"{teamName} Batters {year} {xHeaderName} vs {yHeaderName}"
        
        MAX_SCATTERPLOT_ENTRIES = 12
        if(len(xData) > MAX_SCATTERPLOT_ENTRIES):
            xData = xData[:MAX_SCATTERPLOT_ENTRIES] #cut the list so that it is only 10 elements because as of now, I only want to show up to 10 elements due to it being difficult for each element (dot) to be it's own unique color
            yData = yData[:MAX_SCATTERPLOT_ENTRIES]
            names = names[:MAX_SCATTERPLOT_ENTRIES]
            
        with open(htmlFileName, mode="w") as file:
            file.write(StatsVisualizer.makeScatterplotHTML(DatabaseStatsScraperManager.convertStringsToFloats(xData), DatabaseStatsScraperManager.convertStringsToFloats(yData), xHeaderName, yHeaderName, graphTitle, names))
    
with sqlite3.connect('baseballStats.db') as statsDb:
    thisDatabaseStatsScraperManager = DatabaseStatsScraperManager()
    #thisDatabaseStatsScraperManager.uploadTeamBasicBatterStats(statsDb, "White Sox", "2023")
    
    #thisDatabaseStatsScraperManager.uploadTeamContracts(statsDb, "Red Sox")
    #thisDatabaseStatsScraperManager.uploadAllTeamsContracts(statsDb)
    #thisDatabaseStatsScraperManager.uploadAllTeamsBasicBatterStats(statsDb, "2023")
    
    #statsDb.commit()
    xHeaderName = "Age"
    yHeaderName = "OPSPLUS"
    thisDatabaseStatsScraperManager.makeBasicBatterStatsScatterplotHTML("White Sox", "2023", xHeaderName, yHeaderName)
    
   
   
