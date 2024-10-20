
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





_STATS_VIS_SAVE_PATH = 'website\static\embeddedHTML\statsGraphs\\' 


def convertStringsToFloats(strList):
    floatList = []
    for stringVal in strList:
        try:
            floatList.append(float(stringVal))
        except ValueError:
            floatList.append(float(0))
    return floatList
        
# def makeGraphHTMLFileName(self, )
    
def makeGraphHTML(databaseManager: DatabaseManager, graphInfo: GraphInfo):
    yData = databaseManager.selectBasicBatterStats(statsDb, graphInfo.teamName, graphInfo.year, [graphInfo.yHeaderName])
    xData = databaseManager.selectBasicBatterStats(statsDb, graphInfo.teamName, graphInfo.year, [graphInfo.xHeaderName])
    names = databaseManager.selectBasicBatterStats(statsDb, graphInfo.teamName, graphInfo.year, ["Name"])
    teamNameWithoutSpaces = graphInfo.teamName.replace(" ", "")
    htmlFileName = f"{_STATS_VIS_SAVE_PATH}{teamNameWithoutSpaces}{graphInfo.year}{graphInfo.xHeaderName}Vs{graphInfo.yHeaderName}.html"
    graphTitle = f"{graphInfo.teamName} Batters {graphInfo.year} {graphInfo.xHeaderName} vs {graphInfo.yHeaderName}"
    
    MAX_SCATTERPLOT_ENTRIES = 12
    if(len(xData) > MAX_SCATTERPLOT_ENTRIES):
        xData = xData[:MAX_SCATTERPLOT_ENTRIES] #cut the list so that it is only the amount elements equal to MAX_SCATTERPLOT_ENTRIES because as of now, I only want to show up to this many elements due to it being difficult for each element (dot) to be it's own unique color
        yData = yData[:MAX_SCATTERPLOT_ENTRIES]
        names = names[:MAX_SCATTERPLOT_ENTRIES]
        
    with open(htmlFileName, mode="w") as file:
        args = ScatterplotInfo(convertStringsToFloats(xData), convertStringsToFloats(yData), graphInfo.xHeaderName, graphInfo.yHeaderName, graphTitle, names)
        file.write(stats_visualizer.makeScatterplotHTML(args))
          
          
          
          
            
with sqlite3.connect('baseballStats.db') as statsDb:
    thisDatabaseManager = DatabaseManager()

    # xHeaderName = "Age"
    # yHeaderName = "OPSPLUS"
    # scatterplotArgs = GraphInfo("White Sox", "2023", xHeaderName, yHeaderName, GraphType.SCATTERPLOT) 
    # thisDatabaseManager.makeGraphHTML(scatterplotArgs)