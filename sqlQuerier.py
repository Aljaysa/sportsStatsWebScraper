import sqlite3


import webScraper

deleteAllRecordsPitcherTable = '''DELETE FROM pitchers
                                '''

createPitcherTable = '''CREATE TABLE pitchers (
                        pitcherId INTEGER NOT NULL PRIMARY KEY,
                        name TEXT,
                        age TEXT,
                        games TEXT
                    )'''
                    
createTeamsTable =  '''CREATE TABLE teams (
                        city TEXT NOT NULL PRIMARY KEY,
                        teamName TEXT,
                        wins INTEGER
                    )'''
    
addPitcher = '''INSERT INTO pitchers (name, age, games) VALUES (?, ?, ?)'''

addTeam = '''INSERT INTO teams (city, teamName, wins) VALUES (?, ?, ?)'''

pitchers = [
]
"""
('Marcus', 'Stroman', 'Atlanta', 3.99),
('Chris', 'Sale', 'Boston', 2.65)  
"""

teams = [
    ('Boston', 'Red Sox', 2),
('Toronto', 'Blue Jays', 3) 
]

"""
('Boston', 'Red Sox', 2),
('Toronto', 'Blue Jays', 3) 
"""

_VARCHAR_MAX_STR_LEN = 30
_SPECIAL_CHARS = ("+", "-") #({'`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}','}','|','\',':',';','"',''','<',',','>','.','?','/'})
_SPECIAL_CHAR_REPLACEMENT_STRS = dict([
    ("+", "PLUS"),
    ("-", "MINUS")
])




#@staticmethod
def addUnderscoreToStrsFirstCharNum(strList):
    newStrList = []
    for str in strList:
        try:
            if(str[0].isdigit()):
                newStrList.append("_" + str)
            else:
                newStrList.append(str)
        except IndexError:
            newStrList.append(str)
    return newStrList

#@staticmethod
def addUnderscoreToStrFirstCharNum(str):
        try:
            if(str[0].isdigit()):
                return ("_" + str)
            else:
                return str
        except IndexError:
            return str
        
#@staticmethod
def getReplacedSpecialCharsStr(str):
        if(len(str) == 0):
            return str
        else:
            specialCharsReplacedStr = ""
            for char in str:
                if(char in _SPECIAL_CHARS):
                    try:
                        specialCharsReplacedStr = specialCharsReplacedStr + _SPECIAL_CHAR_REPLACEMENT_STRS[char]
                    except KeyError:
                        specialCharsReplacedStr = specialCharsReplacedStr + "_ERROR:SPECIAL_CHAR_IN_HEADER_NOT_SUPPORTED_"
                else:
                    specialCharsReplacedStr = specialCharsReplacedStr + char
            return specialCharsReplacedStr
        
   

def getCreateTableHeaderDecl(headerName, headerType, isNotNullPrimaryKey=False):
    tableHeaderStr = ""
    if headerType is bool:
        tableHeaderStr = f'{headerName} BOOL'
    elif headerType is int:
        tableHeaderStr = f'{headerName} INT'
    elif headerType is float:
        tableHeaderStr = f'{headerName} FLOAT'
    else:
        tableHeaderStr = f'{headerName} VARCHAR({_VARCHAR_MAX_STR_LEN})' 
    if(isNotNullPrimaryKey):
        tableHeaderStr = tableHeaderStr + " NOT NULL PRIMARY KEY"
    return tableHeaderStr



def getCreateTableHeaderDecls(headerNames, headerTypes):
    for (headerName, headerType) in zip(headerNames, headerTypes):
        headerName = getReplacedSpecialCharsStr(headerName)
        headerName = addUnderscoreToStrFirstCharNum(headerName)
        yield getCreateTableHeaderDecl(headerName, headerType)


def getCreateTableCmd(tableName, headerNames, headerTypes):
    createTableHeaderDecls = getCreateTableHeaderDecls(headerNames, headerTypes)
    createTableCmd = f"CREATE TABLE {tableName} ("
    createTableCmd = createTableCmd + ",\n".join(createTableHeaderDecls)
    createTableCmd = createTableCmd + ")"
    return createTableCmd
         

with sqlite3.connect('baseballStats.db') as statsDb:
    thisBaseballStatsScraper = webScraper.baseballStatsScraper()
    baltimoreOriolesBatterHeaders = thisBaseballStatsScraper.getTeamBatterHeaders("Baltimore", "2023")
    baltimoreOriolesBatterStats = thisBaseballStatsScraper.getTeamBatterStats("Baltimore", "2023")
    baltimoreOriolesBatterHeaderTypes = thisBaseballStatsScraper.getInferredTypesFromStrings(baltimoreOriolesBatterStats[0])
    #print(baltimoreOriolesBatterHeaderTypes)
    createTableCmd = getCreateTableCmd("batters", baltimoreOriolesBatterHeaders, baltimoreOriolesBatterHeaderTypes)
    #print(createTableCmd)
    #texasRangersBatterStats = thisBaseballStatsScraper.getTeamBatterStats("Texas", "2023")
    #thisBasketballStatsScraper = webScraper.basketballStatsScraper()
    #philadelphia76ersStats = thisBasketballStatsScraper.getTeamPerGameStats("Philadelphia", "2023")

    
    #statsDb.execute(createPitcherTable)
    #statsDb.execute(createTeamsTable)
    statsDb.execute(deleteAllRecordsPitcherTable)
    statsDb.execute(createTableCmd)

    
    #for (statVal, type) in zip(baltimoreOriolesBatterStats[0], types):
        #print(f"{statVal} : {type}")
    #print(baltimoreOriolesBatterHeaders)
""" 
    for pitcher in baltimoreOriolesBatterStats:
    #for (idx, pitcher) in enumerate(texasRangersBatterStats):  
    #for (idx, pitcher) in enumerate(philadelphia76ersStats):
        print(pitcher)
        #statsDb.execute(addPitcher, pitcher)
"""         
    

        
""" 
    for team in teams:
        #print(team)
        statsDb.execute(addTeam, team)
"""
 
        
statsDb.commit()




