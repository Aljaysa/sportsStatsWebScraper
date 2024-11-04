
import sqlite3
from dataclasses import dataclass
from enum import Enum

from database_manager import DatabaseManager
import stats_visualizer
from stats_visualizer import ScatterplotInfo

class GraphType(Enum):
    SCATTERPLOT = 1

@dataclass
class GraphInfo:
    teamName: str
    year: int
    xHeaderName: str
    yHeaderName: str
    graphType: GraphType





_STATS_VIS_SAVE_PATH = 'static\embeddedHTML\statsGraphs\\' 
_PLAYER_NAME_COL_LABEL = "Player"


def convertStringsToFloats(strList):
    floatList = []
    for stringVal in strList:
        try:
            floatList.append(float(stringVal))
        except ValueError:
            floatList.append(float(0))
    return floatList
        
def getGraphHTMLFileName(graphInfo: GraphInfo):
    teamNameWithoutSpaces = graphInfo.teamName.replace(" ", "")
    return f"{_STATS_VIS_SAVE_PATH}{teamNameWithoutSpaces}{graphInfo.year}{graphInfo.xHeaderName}Vs{graphInfo.yHeaderName}.html"
    
    
def generateGraphHTML(databaseManager: DatabaseManager, graphInfo: GraphInfo):
    yData = databaseManager.selectBasicBatterStats(graphInfo.teamName, graphInfo.year, [graphInfo.yHeaderName])
    xData = databaseManager.selectBasicBatterStats(graphInfo.teamName, graphInfo.year, [graphInfo.xHeaderName])
    names = databaseManager.selectBasicBatterStats(graphInfo.teamName, graphInfo.year, [_PLAYER_NAME_COL_LABEL])
    htmlFileName = getGraphHTMLFileName(graphInfo)
    graphTitle = f"{graphInfo.teamName} Batters {graphInfo.year} {graphInfo.xHeaderName} vs {graphInfo.yHeaderName}"
    
    MAX_SCATTERPLOT_ENTRIES = 12
    if(len(xData) > MAX_SCATTERPLOT_ENTRIES):
        xData = xData[:MAX_SCATTERPLOT_ENTRIES] #cut the list so that it is only the amount elements equal to MAX_SCATTERPLOT_ENTRIES because as of now, I only want to show up to this many elements due to it being difficult for each element (dot) to be it's own unique color
        yData = yData[:MAX_SCATTERPLOT_ENTRIES]
        names = names[:MAX_SCATTERPLOT_ENTRIES]
        
    with open(htmlFileName, mode="w") as file:
        args = ScatterplotInfo(convertStringsToFloats(xData), convertStringsToFloats(yData), graphInfo.xHeaderName, graphInfo.yHeaderName, graphTitle, names)
        file.write(stats_visualizer.makeScatterplotHTML(args))
              
 
          
def generateGraphHTMLUsingUpdatedDatabase(databaseFileName, teamName, year, xAxis, yAxis, graphType):      
    graphInfo = GraphInfo(teamName, year, xAxis, yAxis, graphType) 
    thisDatabaseManager = DatabaseManager(databaseFileName)
    # update database if possible with up to date stats for the team and year requested, if not, throw exception
    try:
        thisDatabaseManager.uploadTeamBasicBatterStats(teamName, year)
    except Exception as e:
        raise DatabaseUpdateFailedException() from e
        
    try:
        generateGraphHTML(thisDatabaseManager, graphInfo)
    except Exception as e:
        raise GraphGenerationFailedException() from e
        
   
def generateGraphHTMLUsingNonUpdatedDatabase(databaseFileName, teamName, year, xAxis, yAxis, graphType):   
    graphInfo = GraphInfo(teamName, year, xAxis, yAxis, graphType) 
    thisDatabaseManager = DatabaseManager(databaseFileName)
    try:
        generateGraphHTML(thisDatabaseManager, graphInfo)
    except Exception as e:
        raise GraphGenerationFailedException() from e
    
class DatabaseUpdateFailedException(Exception):
    def __init__(self, errors=None):            
        # Call the base class constructor with the parameters it needs
        super().__init__("Database failed to be updated, possibly due to an issue updated the database or scraping the data meant to be added to the database.")
        # Now for your custom code...
        self.errors = errors
        
class GraphGenerationFailedException(Exception):
    def __init__(self, errors=None):            
        # Call the base class constructor with the parameters it needs
        super().__init__("Graph failed to be generated.")
        # Now for your custom code...
        self.errors = errors

#For testing purposes
#generateGraphHTMLUsingUpdatedDatabase("baseballStats.db", "Blue Jays", "2023", "PA", "R", GraphType.SCATTERPLOT)
