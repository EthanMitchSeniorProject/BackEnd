import pyodbc

class SoccerPlayer(object):

    def __init__(self, html_data, team_name):
        
        # Information for connecting to the database server on Microsoft Azure
        server = 'calvinscoutingreport.database.windows.net'
        database = 'ScoutingReport'
        username = 'athlete'
        password = 'calvinscoutingreport123!'
        driver = '{ODBC Driver 13 for SQL Server}'
        self._connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;Server='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
        
        # Dictionary for translating player year
        year_translation = {}
        year_translation["Fr."] = "Freshman"
        year_translation["Fr"] = "Freshman"
        year_translation["So."] = "Sophomore"
        year_translation["So"] = "Sophomore"
        year_translation["Jr."] = "Junior"
        year_translation["Jr"] = "Junior"
        year_translation["Sr"] = "Senior"
        year_translation["Sr."] = "Senior"

        # Parse through to find data
        print("----Start Player Data----")
        self.team_name = team_name

        # Name
        self._name = html_data.find("a").contents[0]
        if self._name.startswith(" "):
            self._name = self._name[1:]
            self._name = self._name.replace("  ", " ")
            self._name = self._name.replace("'", "''")
        
        td_list = html_data.findAll("td")

        # Order of TD elements
        #0 - Number
        self._number = td_list[0].contents[0]

        #1 - Nothing

        #2 - "Fr.", "So.", "Jr.", or "Sr." (Year)
        if (td_list[2].contents[0] in year_translation):
            self._year = year_translation[td_list[2].contents[0]]
        else:
            self._year = td_list[2].contents[0]

        #3 - Position
        if (len(td_list[3].contents) == 0):
            self._position = "Unknown"
        else:
            self._position = td_list[3].contents[0]

        #4 - Games Played
        if "-" in td_list[4].contents[0]:
            self._games_played = 0
        else:
            self._games_played = td_list[4].contents[0].rstrip()

        #5 - Games Started
        if "-" in td_list[5].contents[0]:
            self._games_started = 0
        else:
            self._games_started = td_list[5].contents[0].rstrip()

        #6 - Goals (gathered from the game by game stats)

        #7 - Assists (gathered from the game by game stats)

        #8 - Points
        if "-" in td_list[8].contents[0]:
            self._points = 0
        else:
            self._points = td_list[8].contents[0].rstrip()

        #9 - Shots
        if "-" in td_list[9].contents[0]:
            self._shots = 0
        else:
            self._shots = td_list[9].contents[0].rstrip()

        #10 - Shot percentage (can calculate that if wanted)

        #11 - Shots on goal
        if "-" in td_list[11].contents[0]:
            self._shots_on_goal = 0
        else:
            self._shots_on_goal = td_list[11].contents[0].rstrip()

        #12 - Shots on goal percentage (can calculate that if wanted)

        #13 - Yellow Cards
        if "-" in td_list[13].contents[0]:
            self._yellow_cards = 0
        else:
            self._yellow_cards = td_list[13].contents[0].rstrip()

        #14 - Red Cards
        if "-" in td_list[14].contents[0]:
            self._red_cards = 0
        else:
            self._red_cards = td_list[14].contents[0].rstrip()

        #15 - Pks in form of (<made>-<attempted>)

        #16 - Game Winning Goals
        
        # Output the information gathered from the html input
        print("Name:", self._name)
        print("Year:", self._year)
        print("Position:", self._position)
        print("Games Played:", self._games_played)
        print("Games Started:", self._games_started)
        print("Points:", self._points)
        print("Shots:", self._shots)
        print("Shots On Goal:", self._shots_on_goal)
        print("Yellow Cards:", self._yellow_cards)
        print("Red Cards:", self._red_cards)

        print('------End Player Data------\n\n')

    def getTeamId(self):
        cursor = self._connection.cursor()
        select_id_command = "SELECT id FROM team where school_name = '" + self.team_name + "';"
        cursor.execute(select_id_command)
        row = cursor.fetchone()
        if (row is None) or (row[0] is None):
            select_max_command = "SELECT MAX(id) FROM team;"

            cursor.execute(select_max_command)
            new_id = 0
            row = cursor.fetchone()
            if (row[0] is not None):
                new_id = row[0] + 1

            #Team does not currently exist, need to create it on DB
            insert_command = "INSERT INTO team VALUES (" + str(new_id) + ", '" + self.team_name + "');"
            print(insert_command)
            cursor.execute(insert_command)
            print("completed insert")
            self._connection.commit()
            return new_id
        else:
            #Team exists in DB, return id
            return row[0]

    # Send the Player class information to the database
    def sendToDatabase(self):
        try:
            if self.doesRecordExist():
                cursor = self._connection.cursor()
                sql_command = "UPDATE player SET year = '"+self._year+"', position = '"+self._position+"', games_played = "+str(self._games_played) \
                    +", games_started = "+str(self._games_started)+", points = "+str(self._points)+", shots = "+str(self._shots)+", shots_on_goal = " \
                    +str(self._shots_on_goal)+", yellow_cards = "+str(self._yellow_cards)+", red_cards = "+str(self._red_cards)+" WHERE name = '"+self._name+"';"
                cursor.execute(sql_command)
                self._connection.commit()
            else:
                cursor = self._connection.cursor()
                new_id = self.getMaxId()
                sql_command = "INSERT INTO player VALUES ("+str(new_id)+", '"+str(self.getTeamId())+"', '"+self._name+"', '"+self._year+"', '"+self._position+"', "+str(self._games_played) \
                    +", "+str(self._games_started)+", "+str(self._points)+", "+str(self._shots)+", "+str(self._shots_on_goal)+", "+str(self._yellow_cards)+", "+str(self._red_cards)+");"
                cursor.execute(sql_command)
                self._connection.commit()
        except:
            raise NotImplementedError("Base Soccer Player class cannot send to database")

    # Get the largest id in the player table from the database
    # Used to set the new id for a new player
    def getMaxId(self):
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT MAX(id) FROM player;")
            row = cursor.fetchone()
            if row[0] is None:
                return 0
            return row[0] + 1
        except:
            raise NotImplementedError("Cannot connect to database to get new id")

    # Check if a record exists in the database
    # Determines if we need to run an INSERT query or an UPDATE query
    def doesRecordExist(self):
        try:
            cursor = self._connection.cursor()
            sql_command = "SELECT COUNT(*) FROM player WHERE name = '"+self._name+"';"
            cursor.execute(sql_command)
            row = cursor.fetchone()
            count = row[0]
            if count > 0:
                return True
            return False
        except:
            raise NotImplementedError("Cannot connect to database to see if record exists")

    # Return the full name of the player
    def getFullName(self):
        return self._name