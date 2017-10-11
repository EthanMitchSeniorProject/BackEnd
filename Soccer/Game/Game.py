class Game(object):

    def __init__(self, html_data):

        print("----Start Game Data----")

        teams = html_data.contents[0]

        team_list = teams.split()
        position = team_list.index("at")
        end_index = len(team_list) - 1
        away_team = ""
        home_team = ""

        for x in range(0, position):
            if x > 0:
                away_team = away_team + " "
            away_team = away_team + team_list[x]
        for x in range(position + 1, end_index + 1):
            home_team = home_team + team_list[x]
            if x > position:
                home_team = home_team + " "
        
        date = html_data.find("span").contents[0]

        print("Home Team: ", home_team)
        print("Away Team: ", away_team)
        print("Date: ", date)

        print("----End Game Data----\n\n")

    def sendToDatabase(self):
        raise NotImplementedError("Base Game class cannot send to database")