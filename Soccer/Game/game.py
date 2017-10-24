import pyodbc
server = 'calvinscoutingreport.database.windows.net'
database = 'ScoutingReport'
username = 'athlete'
password = 'calvinscoutingreport123!'
driver = '{ODBC Driver 13 for SQL Server}'
connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;Server='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)

class Game(object):

    def __init__(self, html_data):

        print("----Start Game Data----")
        self.events = []
        self.player_game_data = []

        teams = html_data.contents[0]

        team_list = teams.split()
        position = team_list.index("at")
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
        
        date = html_data.find("span").contents[0]

        print("Home Team: ", self.home_team)
        print("Away Team: ", self.away_team)
        print("Date: ", date)

        print("----End Game Data----\n\n")

    def addEvent(self, new_event):
        self.events.append(new_event)

    def getGameString(self):
        return self.home_team + "-" + self.away_team

    def getHomeTeam(self):
        return self.home_team

    def getVisitingTeam(self):
        return self.away_team

    def isInDatabase(self):
        cursor = connection.cursor()
        sql_command = "SELECT COUNT(*) FROM game where home_team = '" + self.home_team + "' AND away_team = '" + self.away_team + "';"
        print("is in database SQL command: " + sql_command)
        cursor.execute(sql_command)
        row = cursor.fetchone()
        count = row[0]
        return (count > 0)

    def getNewId(self):
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(id) FROM game;")
        row = cursor.fetchone()
        if (row[0] is None):
            return 0

        return row[0] + 1
        
    def sendToDatabase(self):
        sql_command = "INSERT INTO game VALUES (" + str(self.getNewId()) + ", '" + self.home_team + "', '" + self.away_team + "');"
        print("Game SQL command: " + sql_command)
        cursor = connection.cursor()
        cursor.execute(sql_command)
        connection.commit()