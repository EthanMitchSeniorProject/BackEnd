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
        
    def sendToDatabase(self):
        #Check if game already exists in database, if so, skip
        #If data does not already exist, create new entry
        #Add Events
        #Add Player Game Data (if player exists in database)
        raise Exception("unimplemented")