# Necessary import for connecting to the database
import pyodbc

# Necessary connection information
server = 'calvinscoutingreport.database.windows.net'
database = 'ScoutingReport'
username = 'athlete'
password = 'calvinscoutingreport123!'
driver = '{ODBC Driver 13 for SQL Server}'
connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;Server='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)

# Event class
class Event(object):

    def __init__(self, game_id, html_data):
        
        print("-----Start Event Data-----")

        self.game_id = game_id
        self.team_id = 1
        self.rotation = 1

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
            self.server_name = name_list[1] + " " + name_list[0]
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
                self.actor_name = name_list[1] + " " + name_list[0]
            self.actor_id = self.findPlayerId(self.actor_name)
        else:
            self.actor_name = self.server_name
            self.actor_id = self.server_id

        # Team ID (team that served the point)
        self.team_id = self.getTeamId(self.server_name)
        
        # Output information
        print("New Score: ", self.new_score)
        print("Description: ", self.description)
        print("Server Name: ", self.server_name)
        print("Server ID: ", self.server_id)
        print("Actor Name: ", self.actor_name)
        print("Actor ID: ", self.actor_id)
        print("Team ID: ", self.team_id)
        print("Game ID: ", self.game_id)
        print("Play Result: ", self.result)

        print("-----End Event Data-----\n\n")

    # Send the Event information to the database
    def sendtoDatabase(self):
        # Check if in database, if not, continue
        if (self.isInDatabase()):
            return

        # Add to database
        sql_command = "INSERT INTO vball_play VALUES (" + str(self.getNewId()) + ", " + str(self.game_id) + ", " + str(self.team_id) + ", "\
            + str(self.server_id) + ", " + str(self.rotation) + ", '" + self.result + "', " + str(actor_id) + ", '" + str(self.new_score) + \
            "';"
        print("Event insert SQL command: " + sql_command)
        cursor = connection.cursor()
        cursor.execute(sql_command)
        connection.commit() 

    # See if the play is already in the database
    def isInDatabase(self):
        sql_command = "SELECT COUNT(*) FROM vball_play WHERE game_id = " + str(self.game_id) + " AND team_id = '" + self.text\
            + "' AND server_id = '" + self.text + "' AND new_score = '" + self.text + "';"
        cursor = connection.cursor()
        cursor.execute(sql_command)
        row = cursor.fetchone()
        return row[0] > 0

    # Get new Id for a new play
    def getNewId(self):
        sql_command = "SELECT MAX(id) FROM vball_play;"
        cursor = connection.cursor()
        cursor.execute(sql_command)
        row = cursor.fetchone()
        if (row[0] is None):
            return 0
        return row[0] + 1

    # Find id for a given player based on their name
    def findPlayerId(self, name):
        sql_command = "SELECT id FROM vball_player WHERE name = '" + name + "';"
        cursor = connection.cursor()
        cursor.execute(sql_command)
        row = cursor.fetchone()
        if (row is None):
            return None
        return row[0]

    # Find team_id for a given player based on their name
    def getTeamId(self, player_name):
        sql_command = "SELECT school_id FROM vball_player WHERE name = '" + player_name + "';"
        cursor = connection.cursor()
        cursor.execute(sql_command)
        row = cursor.fetchone()
        if (row is None):
            return -1
        return row[0]