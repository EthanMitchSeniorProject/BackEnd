class PlayerGame(object):
    #Init:
    #Player Name (Used to find player.ID)
    #Game Database ID
    #Goals
    #Assists
    #Starter strings (array of two strings that contain the names of each team's starter)

    __init__(self, name, game_id, goals, assists, starter_strings):
        self.name = name
        self.game_id = game_id
        self.goals = goals
        self.assists
        self.started = False
        for start_str in starter_strings:
            if (self.name in start_str):
                self.started = True

    def sendToDatabase(self):
        raise NotImplementedError("No method support for PlayerGame.sendToDatabase() yet...")