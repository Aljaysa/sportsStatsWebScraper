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
    
addPitcher = '''INSERT INTO pitchers (pitcherId, name, age, games) VALUES (?, ?, ?, ?)'''

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

with sqlite3.connect('baseballStats.db') as statsDb:
    thisStatsScraper = webScraper.statsScraper()
    baltimoreOriolesPitcherStats = thisStatsScraper.getBaseballTeamPitcherStats("Texas", "2023")
    
    #statsDb.execute(createPitcherTable)
    #statsDb.execute(createTeamsTable)
    statsDb.execute(deleteAllRecordsPitcherTable)
    for (idx, pitcher) in enumerate(baltimoreOriolesPitcherStats):
        pitcherData = ((idx,) + pitcher)
        #print(pitcherData)
        statsDb.execute(addPitcher, pitcherData)
""""    
    for team in teams:
        #print(team)
        statsDb.execute(addTeam, team)
"""
 
        
statsDb.commit()




