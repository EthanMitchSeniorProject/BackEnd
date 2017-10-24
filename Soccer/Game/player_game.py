class PlayerGame(object):
    #Init:
    #Player Name (Used to find player.ID)
    #Game Database ID
    #Goals
    #Assists
    #Starter strings (array of two strings that contain the names of each team's starter)

    def __init__(self, name, game_id, goals, assists, starter_strings):
        self.name = name
        self.game_id = game_id
        self.goals = goals
        self.assists
        self.started = False
        for start_str in starter_strings:
            if (self.name in start_str):
                self.started = True

    def __findPlayerId():
        cursor = connection.cursor()
        sql_command = "SELECT id FROM player where name = '" + self.name + "';"
        cursor.execute(sql_command)
        row = cursor.fetchone()
        return row[0]


    def sendToDatabase(self):
        start_bit = 0
        if self.started:
            start_bit = 1
        sql_command = "INSERT INTO player_game VALUES (" + self.__findPlayerId() + ", " + self.game_id + ", " + self.goals + ", " + self.assists + ", " + start_bit + ");"
        print("Player game sql command: " + sql_command)
        cursor = connection.cursor()
        cursor.execute(sql_command)
        connection.commit()