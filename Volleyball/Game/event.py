# Necessary import for connecting to the database
import pyodbc
from database_connection import DatabaseConnection

# Event class
class Event(object):

    def __init__(self, game_id, home_team, away_team, html_data, previous_play):
        
        # Information for connecting to the database server on Microsoft Azure
        self._connection = DatabaseConnection.getConnection()
        
        print("-----Start Event Data-----")

        # TODO: Calculate rotation number based on the team that started serving and the points scored
        self.game_id = game_id

        # Store the team name that is not Calvin
        #   Needed to get team id for players that we do not know
        if (home_team.find("Calvin") == -1):
            self.not_calvin_team_name = home_team
        else:
            self.not_calvin_team_name = away_team

        td_list = html_data.findAll("td")

        # General Information
        if (len(td_list[0]) > 0):
            self.new_score = td_list[0].contents[0]
        self.description = td_list[1].contents[0].strip()
        if (len(td_list[2]) > 0):
            self.new_score = td_list[2].contents[0]

        # Server Name and ID
        self.server_name = self.description.split("]")[0]
        self.server_name = self.server_name.replace("[", "").replace("'", "''").strip()
        if (self.server_name.find(",") != -1):
            name_list = self.server_name.split(",")
            self.server_name = name_list[1].strip() + " " + name_list[0].strip()
        self.server_id = self.findPlayerId(self.server_name)

        # Play Result Information
        split_one = self.description.split("]")[1]
        split_two = split_one.split(".")[0].strip()
        possible_results = ["Kill", "Attack error", "Service ace", "Service error", "Bad set", "Ball handling error"]
        for result in possible_results:
            if (split_two.find(result) != -1):
                self.result = result

        # Actor Name and ID
        split_three = self.description.split("]")[1]
        split_four = split_three.split(".")[0].strip()
        if (split_four.find(" by ") != -1):
            split_five = split_four.split(" by ")[1].strip()
            if (split_five.find("(from") != -1):
                self.actor_name = split_five.split("(from")[0].strip().replace("'", "''")
            elif (split_five.find("(block") != -1):
                self.actor_name = split_five.split("(block")[0].strip().replace("'", "''")
            else:
                self.actor_name = split_five.replace("'", "''").strip()
            if (self.actor_name.find(",") != -1):
                name_list = self.actor_name.split(",")
                self.actor_name = name_list[1].strip() + " " + name_list[0]
            self.actor_id = self.findPlayerId(self.actor_name)
        else:
            self.actor_name = self.server_name
            self.actor_id = self.server_id

        # Team ID (team that served the point)
        self.team_id = self.getTeamId(self.server_name)

        # Rotation
        if (previous_play is None):
            self.rotation = 1
        elif (self.new_score == "0-1" or self.new_score == "1-0"):
            self.rotation = 1
            print("FIRST POINT")
        else:
            if (self.team_id == 0):
                if (self.getTeamId(previous_play.returnServerName()) == 0):
                    self.rotation = previous_play.returnRotation()
                else:
                    if (previous_play.returnRotation() == 6):
                        self.rotation = 1
                    else:
                        self.rotation = previous_play.returnRotation() + 1
            else:
                self.rotation = previous_play.returnRotation()
        
        # Output information
        print("New Score: ", self.new_score)
        print("Description: ", self.description)
        print("Rotation: ", self.rotation)
        print("Server Name: ", self.server_name)
        print("Server ID: ", self.server_id)
        print("Team ID: ", self.team_id)
        print("Actor Name: ", self.actor_name)
        print("Actor ID: ", self.actor_id)
        print("Game ID: ", self.game_id)
        print("Play Result: ", self.result)

        print("-----End Event Data-----\n\n")

    # Send the Event information to the database
    def sendToDatabase(self):
        # Add to database
        sql_command = "INSERT INTO vball_play VALUES (" + str(self.getNewId()) + ", " + str(self.game_id) + ", " + str(self.team_id) + ", "\
            + str(self.server_id) + ", " + str(self.rotation) + ", '" + self.result + "', " + str(self.actor_id) + ", '" + str(self.new_score) + \
            "');"
        print("Event insert SQL command: " + sql_command)
        cursor = self._connection.cursor()
        cursor.execute(sql_command)
        self._connection.commit()

    # Get new Id for a new play
    def getNewId(self):
        sql_command = "SELECT MAX(id) FROM vball_play;"
        cursor = self._connection.cursor()
        cursor.execute(sql_command)
        row = cursor.fetchone()
        if (row[0] is None):
            return 0
        return row[0] + 1

    # Find id for a given player based on their name
    def findPlayerId(self, name):
        sql_command = "SELECT id FROM vball_player WHERE name = '" + name + "';"
        cursor = self._connection.cursor()
        cursor.execute(sql_command)
        row = cursor.fetchone()
        if (row is None):
            sql_command2 = "INSERT INTO vball_player VALUES (" + str(self.getMaxId() + 1) + ", " + str(self.getPlayerTeamId()) + ", '" \
                "" + str(name) + "', 'none', 'none', " + str(0) + ", " + str(0) + ", " \
                "" + str(0) + ", " + str(0) + ", " + str(0) + ", " + str(0) + ", " + str(0) + ", " \
                "" + str(0) + ", " + str(0) + ", " + str(0) + ", " + str(0) + ", " + str(0) + ", " + str(0) + ");"
            print(sql_command2)
            cursor.execute(sql_command2)
            self._connection.commit()
        cursor.execute(sql_command)
        row2 = cursor.fetchone()
        return row2[0]

    # Find team_id for a given player based on their name
    def getTeamId(self, player_name):
        sql_command = "SELECT team_id FROM vball_player WHERE name = '" + player_name + "';"
        cursor = self._connection.cursor()
        cursor.execute(sql_command)
        row = cursor.fetchone()
        if (row is None):
            return -1
        return row[0]

    # Get the max id from the vball_player table
    def getMaxId(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT MAX(id) FROM vball_player")
        row = cursor.fetchone()
        if (row[0] is None):
            return -1
        return row[0]

    # Get the team id from the vball_team table for the player being inserted into the player table
    def getPlayerTeamId(self):
        sql_command = "SELECT id FROM vball_team WHERE school_name = '" + self.not_calvin_team_name + "';"
        cursor = self._connection.cursor()
        cursor.execute(sql_command)
        row = cursor.fetchone()
        if (row is None):
            return -1
        return row[0]

    def returnServerName(self):
        return self.server_name

    def returnRotation(self):
        return self.rotation
