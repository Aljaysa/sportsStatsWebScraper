import ast, re


"""A module to manage data (insert, delete, select, etc) in an SQL database
"""
_VARCHAR_MAX_STR_LEN = 30
#_SPECIAL_CHARS = ("+", "-") #({'`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}','}','|','\',':',';','"',''','<',',','>','.','?','/'})
_SPECIAL_CHAR_REPLACEMENT_STRS = dict([
    ("+", "PLUS"),
    ("-", "MINUS"),
    (" ", "_")
])



def _addUnderscoreToStrsFirstCharNum(strList):
    """Gets a list of strings by adding underscores to all strings that start with a number in an input list 
    Args:
        strList (list): list of strings to loop through
    Returns:
        strList: the processed list of strings
    """        
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


def _addUnderscoreToStrFirstCharNum(str):
    """Gets a string by adding an underscore to it if it starts with a number
    Args:
        str (str): input string to check if it starts with a number
    Returns:
        strList: string that has underscore added to it if it starts with a number
    """    
    try:
        if(str[0].isdigit()):
            return ("_" + str)
        else:
            return str
    except IndexError:
        return str
        

def _getReplacedSpecialCharsStr(str):
    """Gets a string by replacing all special chars from an input string with text versions of the special character ex: '+' -> 'PLUS'. No spaces are added to the string
    Args:
        str (str): input string to replace the special characters in it
    Returns:
        str: string with the special chars replaced with text versions of the special character 
    """        
    if(len(str) == 0):
        return str
    else:
        specialCharsReplacedStr = ""
        for char in str:
            if(char in _SPECIAL_CHAR_REPLACEMENT_STRS):
                try:
                    specialCharsReplacedStr = specialCharsReplacedStr + _SPECIAL_CHAR_REPLACEMENT_STRS[char]
                except KeyError:
                    specialCharsReplacedStr = specialCharsReplacedStr + "_ERROR:SPECIAL_CHAR_IN_HEADER_NOT_SUPPORTED_"
            else:
                specialCharsReplacedStr = specialCharsReplacedStr + char
        return specialCharsReplacedStr      


def _getCreateTableHeaderDecl(headerName, headerType, isNotNullPrimaryKey=False):
    """Gets the string of code of a single header/variable being declared in an SQL Create Table statement.
    Args:
        headerName (str): the name of the header to be declared 
        headerType (type): the type of the header (python type, not SQL type as we convert in this function)
        isNotNullPrimaryKey (bool, optional): _description_. Defaults to False.

    Returns:
        str: string of the code of a single header/variable being declared in an SQL Create Table statement. No comma is added at the end of the command. Ex: "pitcherId INTEGER NOT NULL PRIMARY KEY"
    """        
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


def _getCreateTableHeaderDecls(headerNames, headerTypes):
    """Gets the next string of code in a series of (ie. possibly multiple) headers/variables being declared in an SQL Create Table statement. 
    Ex:
    CREATE TABLE teams (
                    city TEXT NOT NULL PRIMARY KEY, <- would return this string first (without the comma) and then return the line below this one the next time you call the function
                    teamName TEXT,
                    wins INTEGER
                )
    Args:
        headerNames (list): list of strings containing the names in order of the headers for the SQL table
        headerTypes (list): list of python types corresponding to the names of the headers for the SQL table
    Yields:
        str: the next string of the code in a series of (ie. possibly multiple) headers/variables being declared in an SQL Create Table statement. No comma is added at the end of the command. Ex: "pitcherId INTEGER NOT NULL PRIMARY KEY"
    """        
    for (headerName, headerType) in zip(headerNames, headerTypes):
        yield _getCreateTableHeaderDecl(headerName, headerType)


def _returnInferredType(toInfer):
    """Gets the inferred type of the contents of a string
    Args:
        toInfer (str): the string to detect/assess its type based on various rules, ex: ".05" and "0.05" both are doubles/floats because they contain a period (and not at the very right hand side). "6f79" would evaluate to a string. For rules, see: https://stackoverflow.com/questions/10261141/determine-type-of-value-from-a-string-in-python
    Returns:
        type: a type object representing the type of the input value
    """        
    if len(toInfer) == 0: return None
    try:
        return type(ast.literal_eval(toInfer))
    except ValueError:
        return type(" ") #returns type str
    except SyntaxError:
        return type(" ") #returns type str


def getCreateTableCmd(tableName, headerNames, headerTypes):
    """Gets the string of code of a SQL Create Table statement for a given set of headers
    Args:
        tableName (str): name of the SQL table
        headerNames (list[str]): a list of strings corresponding to the header names of the SQL table (in order)
        headerTypes (list[str]): a list of python type objects corresponding to the headers of the SQL table (in order)
    Returns:
        str: the SQL CREATE TABLE statement for a given set of headers
    """        
    createTableHeaderDecls = _getCreateTableHeaderDecls(headerNames, headerTypes)
    createTableCmd = f"CREATE TABLE {tableName} ("
    createTableCmd = createTableCmd + ",\n".join(createTableHeaderDecls)
    createTableCmd = createTableCmd + ")"
    return createTableCmd


def getDropTableCmd(tableName):
    """Gets the string of code of a SQL Drop Table statement for a given table name
    Args:
        tableName (str): name of the SQL table
    Returns:
        str: the SQL Drop Table statement
    """        
    return f"DROP TABLE {tableName}"


def getInsertIntoCmd(tableName, headerNames):
    """Gets the string of code of a SQL INSERT INTO statement for a given set of headers
    Args:
        tableName (str): name of the SQL table
        headerNames (list): a list of strings corresponding to the header names of the SQL table (in order)
    Returns:
        str: the SQL INSERT INTO statement for a given set of headers
    """        
    insertIntoCmd = f"INSERT INTO {tableName} ("
    insertIntoCmd = insertIntoCmd + ", ".join(headerNames)
    insertIntoCmd = insertIntoCmd + ") VALUES ("
    questionMarksCommaSep = ", ".join(["?" for i in range(len(headerNames))])
    insertIntoCmd = insertIntoCmd + questionMarksCommaSep + ")"
    return insertIntoCmd    


def formatTableHeaders(unformattedTableHeaders):
    """Takes a list of headers (strings) and formats them so that they are valid/they adhere to the naming constraints of database headers. For naming constraints, see: https://learn.microsoft.com/en-us/sql/relational-databases/databases/database-identifiers?view=sql-server-2017
    Args:
        unformattedTableHeaders (list): list of strings representing the SQL table headers
    Returns:
        list: list of strings, ie. the formatted headers that adhere to the naming constraints of database headers 
    """        
    formattedTableHeaders = []
    for header in unformattedTableHeaders:
        header = _getReplacedSpecialCharsStr(header)
        header = _addUnderscoreToStrFirstCharNum(header)
        formattedTableHeaders.append(header)
    return formattedTableHeaders


def getInferredTypesFromStrings(strList: list[str]) -> list[type]:
    """Gets the inferred types of a set of strings based on a set of rules. For rules, see: https://stackoverflow.com/questions/10261141/determine-type-of-value-from-a-string-in-python
    Args:
        strList (list[str]): list of strings to infer the types of 
    Returns:
        list[type]: the inferred types of the input strings 
    """        
    typeList = [] 
    for str in strList:
        typeList.append(_returnInferredType(str))
        #print(f"{str}: {StatsScraper._returnInferredType(str)}")
    #print(typeList)
    return typeList


def getSelectCmd(tableName, headerNames):
    """Gets the string of code of a SQL SELECT statement for a given set of headers
    Args:
        tableName (str): name of the SQL table
        headerNames (list): a list of strings corresponding to the header names of the SQL table (in order)
    Returns:
        str: the SQL SELECT statement for a given set of headers
    """        
    cmd = "SELECT "
    cmd = cmd + ", ".join(headerNames)
    cmd = cmd + " FROM "
    cmd = cmd + tableName
    return cmd  







