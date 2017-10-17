class Event(object):

    def __init__(self, html_data):

        print("----Start Event Data---")

        team = html_data.find("span").contents[0]

        td_list = html_data.findAll("td")

        #Order of TD elements
        #0 - Time of event
        time = td_list[0].contents[0]
        
        #1 - Text of Event
        text = td_list[1].contents[0]

        #2 - Total Score
        total = td_list[2].contents[0]

        print("Team: ", team)
        print("Time of Event: ", time)
        print("Description of Event: ", text)
        print("Total Score: ", total)

        print("-----End Event Data----\n\n")

    def sendToDatabase(self):
        raise NotImplementedError("Base Game class cannot send to database")