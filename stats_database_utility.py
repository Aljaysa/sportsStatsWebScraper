from typing_extensions import final
import ast, re


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

@final
class StatsDatabaseUtility:
    _VARCHAR_MAX_STR_LEN = 30
    #_SPECIAL_CHARS = ("+", "-") #({'`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}','}','|','\',':',';','"',''','<',',','>','.','?','/'})
    _SPECIAL_CHAR_REPLACEMENT_STRS = dict([
        ("+", "PLUS"),
        ("-", "MINUS"),
        (" ", "_")
    ])


    @staticmethod
    def _addUnderscoreToStrsFirstCharNum(strList):
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

    @staticmethod
    def _addUnderscoreToStrFirstCharNum(str):
            try:
                if(str[0].isdigit()):
                    return ("_" + str)
                else:
                    return str
            except IndexError:
                return str
            
    @staticmethod
    def _getReplacedSpecialCharsStr(str):
            if(len(str) == 0):
                return str
            else:
                specialCharsReplacedStr = ""
                for char in str:
                    if(char in StatsDatabaseUtility._SPECIAL_CHAR_REPLACEMENT_STRS):
                        try:
                            specialCharsReplacedStr = specialCharsReplacedStr + StatsDatabaseUtility._SPECIAL_CHAR_REPLACEMENT_STRS[char]
                        except KeyError:
                            specialCharsReplacedStr = specialCharsReplacedStr + "_ERROR:SPECIAL_CHAR_IN_HEADER_NOT_SUPPORTED_"
                    else:
                        specialCharsReplacedStr = specialCharsReplacedStr + char
                return specialCharsReplacedStr
            
    
    @staticmethod
    def _getCreateTableHeaderDecl(headerName, headerType, isNotNullPrimaryKey=False):
        tableHeaderStr = ""
        if headerType is bool:
            tableHeaderStr = f'{headerName} BOOL'
        elif headerType is int:
            tableHeaderStr = f'{headerName} INT'
        elif headerType is float:
            tableHeaderStr = f'{headerName} FLOAT'
        else:
            tableHeaderStr = f'{headerName} VARCHAR({StatsDatabaseUtility._VARCHAR_MAX_STR_LEN})' 
        if(isNotNullPrimaryKey):
            tableHeaderStr = tableHeaderStr + " NOT NULL PRIMARY KEY"
        return tableHeaderStr


    @staticmethod
    def _getCreateTableHeaderDecls(headerNames, headerTypes):
        for (headerName, headerType) in zip(headerNames, headerTypes):
            yield StatsDatabaseUtility._getCreateTableHeaderDecl(headerName, headerType)

    @staticmethod
    def _getTableHeadersCommaSepStr(headerNames):
        return ", ".join(headerNames)
    
    @staticmethod
    def _returnInferredType(toInfer):
        if len(toInfer) == 0: return None
        try:
            return type(ast.literal_eval(toInfer))
        except ValueError:
            return type(" ")
        except SyntaxError:
            return type(" ")
    

    @staticmethod
    def getCreateTableCmd(tableName, headerNames, headerTypes):
        createTableHeaderDecls = StatsDatabaseUtility._getCreateTableHeaderDecls(headerNames, headerTypes)
        createTableCmd = f"CREATE TABLE {tableName} ("
        createTableCmd = createTableCmd + ",\n".join(createTableHeaderDecls)
        createTableCmd = createTableCmd + ")"
        return createTableCmd
    
    @staticmethod
    def getDropTableCmd(tableName):
        return f"DROP TABLE {tableName}"
    
    @staticmethod
    def getInsertIntoCmd(tableName, headerNames):
        insertIntoCmd = f"INSERT INTO {tableName} ("
        insertIntoCmd = insertIntoCmd + StatsDatabaseUtility._getTableHeadersCommaSepStr(headerNames)
        insertIntoCmd = insertIntoCmd + ") VALUES ("
        questionMarksCommaSep = ", ".join(["?" for i in range(len(headerNames))])
        insertIntoCmd = insertIntoCmd + questionMarksCommaSep + ")"
        return insertIntoCmd
        

    @staticmethod
    def formatTableHeaders(unformattedTableHeaders):
        formattedTableHeaders = []
        for header in unformattedTableHeaders:
            header = StatsDatabaseUtility._getReplacedSpecialCharsStr(header)
            header = StatsDatabaseUtility._addUnderscoreToStrFirstCharNum(header)
            formattedTableHeaders.append(header)
        return formattedTableHeaders


    
    @staticmethod
    def getInferredTypesFromStrings(strList: list[str]) -> list[type]:
        typeList = [] 
        for str in strList:
            typeList.append(StatsDatabaseUtility._returnInferredType(str))
            #print(f"{str}: {StatsScraper._returnInferredType(str)}")
        #print(typeList)
        return typeList




