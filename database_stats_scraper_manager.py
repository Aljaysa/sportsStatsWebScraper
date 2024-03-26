import sqlite3

from stats_database_utility import StatsDatabaseUtility as StatsDatabaseUtility
from stats_scraper import StatsScraper as StatsScraper
from stats_scraper import BaseballStatsScraper as BaseballStatsScraper
from stats_scraper import BasketballStatsScraper as BasketballStatsScraper

class DatabaseStatsScraperManager():
    def __init__(self):
        self.baseballStatsScraper = BaseballStatsScraper()

    def uploadTeamBasicBatterStats(self, database, year, teamName):   
        tableName = f"{(self.baseballStatsScraper._teamCities[teamName]).capitalize()}BasicBatterStats"
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
            
    def uploadTeamBatterContracts(self, database, teamName):   
        tableName = f"{(self.baseballStatsScraper._teamCities[teamName]).capitalize()}Contracts"
        headers = StatsDatabaseUtility.formatTableHeaders(self.baseballStatsScraper.getTeamContractHeaders(teamName))
        #print(headers)
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
            print(statRow)
            database.execute(insertIntoTableCmd, statRow)
            
    def uploadAllTeamsBasicBatterStatsContracts(self, database, year):
        for teamName in self.baseballStatsScraper._teamCities:
            self.uploadTeamBatterStatsContracts(database, year, teamName)


with sqlite3.connect('baseballStats.db') as statsDb:
    thisDatabaseStatsScraperManager = DatabaseStatsScraperManager()
    thisDatabaseStatsScraperManager.uploadTeamBasicBatterStats(statsDb, "2023", "Orioles")
    thisDatabaseStatsScraperManager.uploadTeamBatterContracts(statsDb, "Orioles")
    #thisDatabaseStatsScraperManager.uploadAllTeamsBatterStatsContracts(statsDb, "2023")
    statsDb.commit()