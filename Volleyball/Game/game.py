# Necessary import for connecting to the database
import pyodbc

# Necessary connection information for connecting to the database
server = 'calvinscoutingreport.database.windows.net'
database = 'ScoutingReport'
username = 'athlete'
password = 'calvinscoutingreport123!'
driver = '{ODBC Driver 13 for SQL Server}'
connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;Server='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)

# Game class
class Game(object):

    def __init__(self, html_data):

        self._id = -1
        print("----Start Game Data----")
        self.events = []

        teams = html_data.find("strong").contents[0]

        team_list = teams.split()
        if ("at" in team_list):
            position = team_list.index("at")
        else:
            position = team_list.index("vs.")
        end_index = len(team_list) - 1
        self.away_team = ""
        self.home_team = ""

        for x in range(0, position):
            if x > 0:
                self.away_team = self.away_team + " "
            self.away_team = self.away_team + team_list[x]
        for x in range(position + 1, end_index + 1):
            self.home_team = self.home_team + team_list[x]
            if x > position:
                self.home_team = self.home_team + " "

        self.home_team = self.home_team.strip()
        self.away_team = self.away_team.strip()

        print("Home Team: ", self.home_team)
        print("Away Team: ", self.away_team)
        #print("Date: ", date)

        print("----End Game Data----\n\n")

    # Add an Event to the list of Game Events
    def addEvent(self, new_event):
        self.events.append(new_event)

    # Send the Game and all its information to the database
    def sendToDatabase(self):
        sql_command = "INSERT INTO vball_game VALUES (" + str(self.getNewId()) + ", '" + str(self.getTeamId(self.home_team)) + "', '" + str(self.getTeamId(self.away_team)) + "');"
        print("Game SQL command: " + sql_command)
        cursor = connection.cursor()
        cursor.execute(sql_command)
        connection.commit()

        for e in self.events:
            e.sendToDatabase()

    def isInDatabase():
        cursor = connection.cursor()
        sql_command = "SELECT COUNT(*) FROM vball_game where home_team = '" + str(self.getTeamId(self.home_team)) + "' AND away_team = '" + str(self.getTeamId(self.away_team)) + "';"
        print("Is in database SQL command: " + sql_command)
        cursor.execute(sql_command)
        row = cursor.fetchone()
        count = row[0]
        return (count > 0)

    def getTeamId(self, team):
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM vball_team where school_name = '" + self.team + "'")
        row = cursor.fetchone()
        if (row is None) or (row[0] is None):
            select_max_command = "SELECT MAX(id) FROM team;"

            cursor.execute(select_max_command)
            new_id = 0
            row = cursor.fetchone()
            if (row[0] is not None):
                new_id = row[0] + 1

            #Team does not currently exist, need to create it on DB
            insert_command = "INSERT INTO vball_team VALUES (" + str(new_id) + ", '" + self.team + "');"
            print(insert_command)
            cursor.execute(insert_command)
            print("completed")
            self._connection.commit()
            return new_id
        else:
            return row[0]

    def getNewId(self):
        if self._id != -1:
            return self._id

        cursor = connection.cursor()
        cursor.execute("SELECT MAX(id) FROM vball_game;")
        row = cursor.fetchone()
        if (row[0] is None):
            self._id = 0
        else:
            self._id = row[0] + 1
        return self._id