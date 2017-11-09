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

        # Get the tag that has the team names in it
        teams = html_data.find("strong").contents[0]

        # Split the team names into two team names
        team_list = teams.split()
        if ("at" in team_list):
            position = team_list.index("at")
        else:
            position = team_list.index("vs.")
        end_index = len(team_list) - 1
        self.away_team = ""
        self.home_team = ""

        # Set the home team and away team names
        for x in range(0, position):
            if x > 0:
                self.away_team = self.away_team + " "
            self.away_team = self.away_team + team_list[x]
        for x in range(position + 1, end_index + 1):
            self.home_team = self.home_team + team_list[x]
            if x > position:
                self.home_team = self.home_team + " "

        # Remove whitespace, make it title string format, and replace all ' with '' for SQL purposes
        self.home_team = self.home_team.strip().title().replace("'", "''")
        self.away_team = self.away_team.strip().title().replace("'", "''")

        # Remove "College" or "University" from any of the team names
        if (self.home_team.find("College") != -1):
            temp_team = self.home_team.split("College")[0].strip()
            self.home_team = temp_team

        if (self.home_team.find("University") != -1):
            temp_team = self.home_team.split("University")[0].strip()
            self.home_team = temp_team

        if (self.away_team.find("College") != -1):
            temp_team = self.away_team.split("College")[0].strip()
            self.away_team = temp_team

        if (self.away_team.find("University") != -1):
            temp_team = self.away_team.split("University")[0].strip()
            self.away_team = temp_team

        # Get the team id from the database
        self.home_team_id = self.getTeamId(self.home_team)
        self.away_team_id = self.getTeamId(self.away_team)

        print("Home Team: ", self.home_team)
        print("Home Team Id: ", self.home_team_id)
        print("Away Team: ", self.away_team)
        print("Away Team Id: ", self.away_team_id)

        print("----End Game Data----\n\n")

    # Add an Event to the list of Game Events
    def addEvent(self, new_event):
        self.events.append(new_event)

    # Send the Game and all its information to the database
    def sendToDatabase(self):
        # Check if in database, if not, continue
        if (self.isInDatabase()):
            return
        
        # Add to Database
        sql_command = "INSERT INTO vball_game VALUES (" + str(self.getNewId()) + ", " + str(self.home_team_id) + ", " + str(self.away_team_id) + ");"
        print("Game SQL command: " + sql_command)
        cursor = connection.cursor()
        cursor.execute(sql_command)
        connection.commit()

        for e in self.events:
            e.sendToDatabase()

    # Check if the game is already in the database...
    #   If so, do not insert into database again.
    def isInDatabase(self):
        cursor = connection.cursor()
        sql_command = "SELECT COUNT(*) FROM vball_game where home_team = '" + str(self.home_team_id) + "' AND away_team = '" + str(self.away_team_id) + "';"
        print("Is in database SQL command: " + sql_command)
        cursor.execute(sql_command)
        row = cursor.fetchone()
        count = row[0]
        return (count > 0)

    # Get the team id for the game class
    def getTeamId(self, team):
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM vball_team where school_name = '" + team + "'")
        row = cursor.fetchone()
        if (row is None) or (row[0] is None):
            select_max_command = "SELECT MAX(id) FROM vball_team;"

            cursor.execute(select_max_command)
            new_id = 0
            row = cursor.fetchone()
            if (row[0] is not None):
                new_id = row[0] + 1

            #Team does not currently exist, need to create it on DB
            insert_command = "INSERT INTO vball_team VALUES (" + str(new_id) + ", '" + team + "');"
            print(insert_command)
            cursor.execute(insert_command)
            connection.commit()
            return new_id
        else:
            return row[0]

    # Get the new id (1 more than the current max id) for a game record
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

    # Return the home team name
    def getHomeTeam(self):
        return self.home_team

    # Return the away team name
    def getAwayTeam(self):
        return self.away_team