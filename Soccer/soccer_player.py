import pyodbc
server = 'calvinscoutingreport.database.windows.net'
database = 'ScoutingReport'
username = 'athlete'
password = 'calvinscoutingreport123!'
driver = '{ODBC Driver 13 for SQL Server}'
connection = pyodbc.connect('DRIVER='+driver+';PORT=1433;Server='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)

class SoccerPlayer(object):

    def __init__(self, html_data):
        year_translation = {}

        year_translation["Fr."] = "Freshman"
        year_translation["So."] = "Sophomore"
        year_translation["Jr."] = "Junior"
        year_translation["Sr."] = "Senior"

        #parse through to find data
        print("----Start Player Data----")
        #Name
        self._name = html_data.find("a").contents[0]
        if self._name.startswith(" "):
            self._name = self._name[1:]
        print(self._name)
        
        td_list = html_data.findAll("td")

        #Order of TD elements
        #0 - Number
        self._number = td_list[0].contents[0]

        #1 - Nothing

        #2 - "Fr.", "So.", "Jr.", or "Sr." (Year)
        if (td_list[2].contents[0] in year_translation):
            self._year = year_translation[td_list[2].contents[0]]
        else:
            self._year = td_list[2].contents[0]

        #3 - Position

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

        #6 - Goals

        #7 - Assists

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

        #10 - Shot percentage (don't need, we can calculate that if wanted)

        #11 - Shots on goal
        if "-" in td_list[11].contents[0]:
            self._shots_on_goal = 0
        else:
            self._shots_on_goal = td_list[11].contents[0].rstrip()

        #12 - Shots on goal percentage (same as 10)

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

        self._position = 'temp'
        
        print("Name:", self._name)
        print("Year:", self._year)
        print("Games Played:", self._games_played)
        print("Games Started:", self._games_started)
        print("Points:", self._points)
        print("Shots:", self._shots)
        print("Shots On Goal:", self._shots_on_goal)
        print("Yellow Cards:", self._yellow_cards)
        print("Red Cards:", self._red_cards)
        print('------End Player Data------\n\n')

    def sendToDatabase(self):
        try:
            if self.doesRecordExist():
                cursor = connection.cursor()
                sql_command = "UPDATE player SET year = '"+self._year+"', position = '"+self._position+"', games_played = "+str(self._games_played)+", games_started = "+str(self._games_started)+", points = "+str(self._points)+", shots = "+str(self._shots)+", shots_on_goal = "+str(self._shots_on_goal)+", yellow_cards = "+str(self._yellow_cards)+", red_cards = "+str(self._red_cards)+" WHERE name = '"+self._name+"';"
                #print(sql_command)
                cursor.execute(sql_command)
                connection.commit()
            else:
                cursor = connection.cursor()
                new_id = self.getMaxId()
                sql_command = "INSERT INTO player VALUES ("+str(new_id)+", '"+self._name+"', '"+self._year+"', '"+self._position+"', "+str(self._games_played)+", "+str(self._games_started)+", "+str(self._points)+", "+str(self._shots)+", "+str(self._shots_on_goal)+", "+str(self._yellow_cards)+", "+str(self._red_cards)+");"
                #print(sql_command)
                cursor.execute(sql_command)
                connection.commit()
        except:
            raise NotImplementedError("Base Soccer Player class cannot send to database")

    def getMaxId(self):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(id) FROM player;")
            row = cursor.fetchone()
            return row[0] + 1
        except:
            raise NotImplementedError("Cannot connect to database to get new id")

    def doesRecordExist(self):
        try:
            cursor = connection.cursor()
            sql_command = "SELECT COUNT(*) FROM player WHERE name = '"+self._name+"';"
            cursor.execute(sql_command)
            row = cursor.fetchone()
            count = row[0]
            if count > 0:
                return True
            return False
        except:
            raise NotImplementedError("Cannot connect to database to see if record exists")

    def getFullName(self):
        return self._name