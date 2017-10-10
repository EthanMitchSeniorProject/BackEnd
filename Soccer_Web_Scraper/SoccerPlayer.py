class SoccerPlayer(object):

    def __init__(self, html_data):
        year_translation = {}

        year_translation["Fr."] = "Freshman"
        year_translation["So."] = "Sophomore"
        year_translation["Jr."] = "Junior"
        year_translation["Sr."] = "Senior"

        #parse through to find data
        print("----Start Player Data")
        #Name
        name = html_data.find("a").contents[0]
        if name.startswith(" "):
            name = name[1:]
        print(name)
        
        td_list = html_data.findAll("td")
        #Order of TD elements
        #0 - Number
        number = td_list[0].contents[0]
        #1 - Nothing
        #2 - "Fr.", "So.", "Jr.", or "Sr." (Year)
        if (td_list[2].contents[0] in year_translation):
            year = year_translation[td_list[2].contents[0]]
        else:
            year = td_list[2].contents[0]
        #3 - Position
        #4 - Games Played
        games_played = td_list[4].contents[0]
        #5 - Games Started
        games_started = td_list[5].contents[0]
        #6 - Goals
        goals = td_list[6].contents[0]
        #7 - Assists
        assists = td_list[7].contents[0]
        #8 - Points
        points = td_list[8].contents[0]
        #9 - Shots
        shots = td_list[9].contents[0]
        #10 - Shot percentage (don't need, we can calculate that if wanted)
        #11 - Shots on goal
        shots_on_goal = td_list[11].contents[0]
        #12 - Shots on goal percentage (same as 10)
        #13 - Yellow Cards
        yellow_cards = td_list[13].contents[0]
        #14 - Red Cards
        red_cards = td_list[14].contents[0]
        #15 - Pks in form of (<made>-<attempted>)
        #16 - Game Winning Goals
        
        print("Name:", name)
        print("Year:", year)
        print("Games Played:", games_played)
        print("Games Started:", games_started)
        print("Goals:", goals)
        print("Asissts:", assists)
        print("Points:", points)
        print("Shots:", shots)
        print("Shots On Goal:", shots_on_goal)
        print("Yellow Cards:", yellow_cards)
        print("Red Cards:", red_cards)
        print('------End Player Data------\n\n')

    def sendToDatabase(self):
        raise NotImplementedError("Base Player class cannot send to database")

    def getFullName(self):
        return self.first_name + self.last_name