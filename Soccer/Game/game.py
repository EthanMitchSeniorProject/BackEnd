import pyodbc
from date_converter import DateConverter
from database_connection import DatabaseConnection

connection = DatabaseConnection.getConnection()

class Game(object):
    def __init__(self, html_data):

        self._id = -1
        print("----Start Game Data----")
        self.events = []

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

        self.home_team = self.home_team.strip()
        self.away_team = self.away_team.strip()

        self.date = DateConverter.convertStringToDate(html_data.find("span").contents[0])

        print("Home Team: ", self.home_team)
        print("Away Team: ", self.away_team)
        print("Date: ", self.date)

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
        sql_command = "SELECT COUNT(*) FROM game where home_team = '" + str(self.getTeamId(self.home_team)) + "' AND away_team = '" + str(self.getTeamId(self.away_team)) + "' AND game_date = '" + self.date + "';"
        print("is in database SQL command: " + sql_command)
        cursor.execute(sql_command)
        row = cursor.fetchone()
        count = row[0]
        return (count > 0)

    def getNewId(self):
        if self._id != -1:
            return self._id

        cursor = connection.cursor()
        cursor.execute("SELECT MAX(id) FROM game;")
        row = cursor.fetchone()
        if (row[0] is None):
            self._id = 0
        else:
            self._id = row[0] + 1
        return self._id


    def getTeamId(self, team):
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM team where school_name = '" + team + "'")
        row = cursor.fetchone()
        if (row is None) or (row[0] is None):
            select_max_command = "SELECT MAX(id) FROM team;"

            cursor.execute(select_max_command)
            new_id = 0
            row = cursor.fetchone()
            if (row[0] is not None):
                new_id = row[0] + 1

            #Team does not currently exist, need to create it on DB
            insert_command = "INSERT INTO team(id, school_name) VALUES (" + str(new_id) + ", '" + team + "');"
            print(insert_command)
            cursor.execute(insert_command)
            print("completed")
            connection.commit()
            return new_id
        else:
            return row[0]

        
    def sendToDatabase(self):
        sql_command = "INSERT INTO game VALUES (" + str(self.getNewId()) + ", '" + str(self.getTeamId(self.home_team)) + "', '" + str(self.getTeamId(self.away_team)) + "', '" + self.date + "');"
        print("Game SQL command: " + sql_command)
        cursor = connection.cursor()
        cursor.execute(sql_command)
        connection.commit()

        for e in self.events:
            e.sendToDatabase()