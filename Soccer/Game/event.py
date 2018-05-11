import pyodbc
from Utilities.database_connection import DatabaseConnection

connection = DatabaseConnection.getConnection()

class Event(object):

    def __init__(self, game_id, html_data):

        print("----Start Event Data---")

        self.game_id = game_id
        self.team = html_data.find("span").contents[0]

        td_list = html_data.findAll("td")

        #Order of TD elements
        #0 - Time of event
        self.time = td_list[0].contents[0].replace(" ", "")
        
        #1 - Text of Event
        self.text = td_list[1].contents[0].replace("'", "''")

        #2 - Total Score
        self.total = td_list[2].contents[0]

        print("Team: ", self.team)
        print("Time of Event: ", self.time)
        print("Description of Event: ", self.text)
        print("Total Score: ", self.total)

        print("-----End Event Data----\n\n")

    def isInDatabase(self):
        sql_command = "SELECT COUNT(*) FROM event WHERE game_id = " + str(self.game_id) + " AND description_event = '" + self.text + "';"
        cursor = connection.cursor()
        cursor.execute(sql_command)
        row = cursor.fetchone()
        return row[0] > 0

    def getNewId(self):
        sql_command = "SELECT MAX(id) FROM event;"
        cursor = connection.cursor()
        cursor.execute(sql_command)
        row = cursor.fetchone()
        if (row[0] is None):
            return 0
        return row[0] + 1

    def getTeamId(self, team):
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM team where school_name = '" + self.team + "'")
        row = cursor.fetchone()
        if (row is None) or (row[0] is None):
            select_max_command = "SELECT MAX(id) FROM team;"

            cursor.execute(select_max_command)
            new_id = 0
            row = cursor.fetchone()
            if (row[0] is not None):
                new_id = row[0] + 1

            #Team does not currently exist, need to create it on DB
            insert_command = "INSERT INTO team VALUES (" + str(new_id) + ", '" + self.team + "');"
            print(insert_command)
            cursor.execute(insert_command)
            print("completed")
            self._connection.commit()
            return new_id
        else:
            return row[0]

    def sendToDatabase(self):
        #Check if in database, if not, continue
        if (self.isInDatabase()):
            return

        #Add to database
        sql_command = "INSERT INTO event VALUES (" + str(self.getNewId()) + ", " + str(self.game_id) + ", '" + str(self.getTeamId(self.team)) + "', '" + self.time + "', '" + self.text + "');"
        print("Event insert SQL command: " + sql_command)
        cursor = connection.cursor()
        cursor.execute(sql_command)
        connection.commit() 