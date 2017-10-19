class VolleyballPlayer(object):

    def __init__(self, html_data):
        year_translation = {}

        year_translation["Fr."] = "Freshman"
        year_translation["So."] = "Sophomore"
        year_translation["Jr."] = "Junior"
        year_translation["Sr."] = "Senior"

        #parse through to find data
        print("----Start Player Data----")

        #Name
        name = html_data.find("a").contents[0]
        if name.startswith(" "):
            name = name[1:]
        print(name)

        td_list = html_data.findAll("td")

        #Order of TD elements
        #0 - Number
        if len(td_list[0]) > 0:
            number = td_list[0].contents[0]
        else:
            number = ''
        #1 - Nothing
        #2 - Year
        if (td_list[2].contents[0] in year_translation):
            year = year_translation[td_list[2].contents[0]]
        else:
            year = td_list[2].contents[0]
        #3 - Position

        #4 - Matches Played
        matches_played = td_list[4].contents[0]
        #5 - Sets Played
        sets_played = td_list[5].contents[0]
        #6 - Kills
        kills = td_list[6].contents[0]
        #7 - Kills per Set
        #8 - Errors
        errors = td_list[8].contents[0]
        #9 - Attempts
        attempts = td_list[9].contents[0]
        #10 - Hitting Percentage
        hitting_perc = td_list[10].contents[0]
        #11 - Assists
        assists = td_list[11].contents[0]
        #12 - Assists per Set
        #13 - Service Aces
        services_aces = td_list[13].contents[0]
        #14 - Serivce Aces per Set
        #15 - Digs
        digs = td_list[15].contents[0]
        #16 - Digs per Set
        #17 - Block Solo
        solo_blocks = td_list[17].contents[0]
        #18 - Block Assists
        block_assists = td_list[18].contents[0]
        #19 - Total Blocks
        #20 - Blocks per Set
        #21 - Points
        points = td_list[21].contents[0]
        #22 - Points per Set

        print("Name:", name)
        print("Number:", number)
        print("Year:", year)
        print("Matches Played:", matches_played)
        print("Sets Played:", sets_played)
        print("Kills:", kills)
        print("Errors:", errors)
        print("Attempts:", attempts)
        print("Hitting Percentage:", hitting_perc)
        print("Assists:", assists)
        print("Service Aces:", services_aces)
        print("Digs:", digs)
        print("Block Solo:", solo_blocks)
        print("Block Assists:", block_assists)
        print("Points:", points)

        print('------End Player Data------\n\n')

    def sendToDatabase(self):
        raise NotImplementedError("Base Volleyball Player class cannot send to database")

    def getFullName(self):
        return self.first_name + self.last_name