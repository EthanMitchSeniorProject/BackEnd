import pyodbc
from database_connection import DatabaseConnection

class VolleyballPlayer(object):

    def __init__(self, html_data, team_name):
        
        # Information for connecting to the database server on Microsoft Azure
        self._connection = DatabaseConnection.getConnection()

        year_translation = {}

        year_translation["Fr."] = "Freshman"
        year_translation["So."] = "Sophomore"
        year_translation["Jr."] = "Junior"
        year_translation["Sr."] = "Senior"
        self.team_name = team_name

        #parse through to find data
        print("----Start Player Data----")

        #Name
        self.name = html_data.find("a").contents[0].strip().replace("  ", " ").replace("'", "''")

        print(self.name)

        td_list = html_data.findAll("td")

        #Order of TD elements
        #0 - Number
        if len(td_list[0]) > 0:
            self.number = td_list[0].contents[0]
        else:
            self.number = -1
            
        #1 - Nothing
        #2 - Year
        if (td_list[2].contents[0] in year_translation):
            self.year = year_translation[td_list[2].contents[0]]
        else:
            self.year = td_list[2].contents[0]
        #3 - Position
        if (len(td_list[3].contents) > 0):
            self.position = td_list[3].contents[0]
        else:
            self.position = "None"
        #4 - Matches Played
        self.matches_played = td_list[4].contents[0]
        #5 - Sets Played
        self.sets_played = td_list[5].contents[0]
        #6 - Kills
        self.kills = td_list[6].contents[0]
        #7 - Kills per Set
        #8 - Errors
        self.errors = td_list[8].contents[0]
        #9 - Attempts
        self.attempts = td_list[9].contents[0]
        #10 - Hitting Percentage
        self.hitting_perc = td_list[10].contents[0]
        #11 - Assists
        self.assists = td_list[11].contents[0]
        #12 - Assists per Set
        #13 - Service Aces
        self.services_aces = td_list[13].contents[0]
        #14 - Serivce Aces per Set
        #15 - Digs
        self.digs = td_list[15].contents[0]
        #16 - Digs per Set
        #17 - Block Solo
        self.solo_blocks = td_list[17].contents[0]
        #18 - Block Assists
        self.block_assists = td_list[18].contents[0]
        #19 - Total Blocks
        #20 - Blocks per Set
        #21 - Points
        self.points = td_list[21].contents[0]
        #22 - Points per Set

        print("Name:", self.name)
        print("Team:", team_name)
        print("Number:", self.number)
        print("Position:", self.position)
        print("Year:", self.year)
        print("Matches Played:", self.matches_played)
        print("Sets Played:", self.sets_played)
        print("Kills:", self.kills)
        print("Errors:", self.errors)
        print("Attempts:", self.attempts)
        print("Hitting Percentage:", self.hitting_perc)
        print("Assists:", self.assists)
        print("Service Aces:", self.services_aces)
        print("Digs:", self.digs)
        print("Block Solo:", self.solo_blocks)
        print("Block Assists:", self.block_assists)
        print("Points:", self.points)

        print('------End Player Data------\n\n')
        
    def getTeamId(self):
        cursor = self._connection.cursor()
        select_id_command = "SELECT id FROM vball_team WHERE school_name = '" + self.team_name + "';"
        cursor.execute(select_id_command)
        row = cursor.fetchone()
        if (row is None) or (row[0] is None):
            select_max_command = "SELECT MAX(id) FROM vball_team;"

            cursor.execute(select_max_command)
            new_id = 0
            row = cursor.fetchone()
            if (row[0] is not None):
                new_id = row[0] + 1

            #Team does not currently exist, need to create it on DB
            insert_command = "INSERT INTO vball_team VALUES (" + str(new_id) + ", '" + self.team_name + "');"
            print(insert_command)
            cursor.execute(insert_command)
            print("completed")
            self._connection.commit()
            return new_id
        else:
            #Team exists in DB, return id
            return row[0]

    def getMaxId(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT MAX(id) FROM vball_player")
        row = cursor.fetchone()
        if (row[0] is None):
            return -1
        
        return row[0]

    def doesRecordExist(self):
        cursor = self._connection.cursor()
        sql_command = "SELECT COUNT(*) FROM vball_player WHERE name = '" + self.name + "';"
        print(sql_command)
        cursor.execute(sql_command)
        print("completed")
        row = cursor.fetchone()
        count = row[0]

        return (count > 0)

    def sendToDatabase(self):
        cursor = self._connection.cursor()
        if self.doesRecordExist():
            sql_command = ("UPDATE vball_player SET num = " + self.number + ", year = '" + self.year + "', position = '" + self.position + 
                "', matches_played = " + self.matches_played + ", sets_played = " + self.sets_played + ", kills = " + 
                self.kills + ", errors = " + self.errors + ", attempts = " + self.attempts + ", hitting_perc = " + 
                self.hitting_perc + ", assists = " + self.assists + ", service_aces = " + self.services_aces + ", digs = " + 
                self.digs + ", solo_blocks = " + self.solo_blocks + ", block_assists = " + self.block_assists + ", points = " + 
                self.points + ", num = " + self.number + " WHERE name = '" + self.name + "';")
        else:
            sql_command = "INSERT INTO vball_player VALUES (" + str(self.getMaxId() + 1) + ", " + str(self.getTeamId()) + ", '" \
                "" + str(self.name) + "', '" + str(self.year) + "', '"+ str(self.position) + "', " + str(self.matches_played) + ", " + str(self.sets_played) + ", " \
                "" + str(self.kills) + ", " + str(self.errors) + ", " + str(self.attempts) + ", " + str(self.hitting_perc) + ", " + str(self.assists) + ", " \
                "" + str(self.services_aces) + ", " + str(self.digs) + ", " + str(self.solo_blocks) + ", " + str(self.block_assists) + ", " + str(self.points) + ", " + str(self.number) + ");"
            
        sql_command = sql_command.replace("-", "0")
        print(sql_command)
        cursor.execute(sql_command)
        self._connection.commit()

    def getFullName(self):
        return self.first_name + self.last_name