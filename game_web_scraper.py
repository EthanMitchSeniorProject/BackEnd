import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
import requests
import json
from Soccer.Game.event import Event
from Soccer.Game.game import Game
from Soccer.Game.player_game import PlayerGame

#This method takes in a beautiful soup element
#and checks to see if the time stamp is at half-time.
#If so, this will contain the starting lineup information
#Verified with Calvin, Kzoo, Hope, Tufts, etc. 
def checkForHalfTime(log_element):
    time = log.find("td", { "class" : "time" })
    return ((time is not None) and (len(time.contents) > 0) and ("45:00" in time.contents[0]))

#This is a method because the same code is used for both home and away teams
#The table_class_string param specifies which table, home or visiting, to look for
def collectPlayerGameData(soup, table_class_string, team_name, game_id, starter_strings):
    if not team_name.lower().replace(" ", "") in teams_collecting:
        print("Not collecting data for: " + team_name + " - " + str(len(team_name)))
        return

    player_game_list = []
    game_stat_summary = soup.find("div", { "class" : table_class_string})
    player_list = game_stat_summary.findAll("tr")
    for player in player_list:
        player_name = player.find("a", { "class" : "player-name"})
        if (player_name is None):
            player_name = player.find("span", { "class" : "player-name"})
        player_stats = player.findAll("td")
        if (len(player_stats) == 0) or (player_name is None) or ("team" in str(player_name).lower()):
            continue
        #0 - Shots
        #1 - Shots on Goal
        #2 - Goals
        #3 - Assists

        print(player_name.contents[0])
        print(player_stats[2].contents[0])
        print(player_stats[3].contents[0])
        player_game = PlayerGame(player_name.contents[0], game_id, player_stats[2].contents[0], player_stats[3].contents[0], starter_strings)
        player_game.sendToDatabase()


#schedule page
soccer_pages = json.loads(requests.get("http://localhost:3000/soccer/teams").text)
website_list = []

for page in soccer_pages:
    if page["url_route"] is None:
        continue
    
    end_index = page["url_route"].find("com/")
    if end_index == -1:
        end_index = page["url_route"].find("edu/")

    website_list.append(page["url_route"][:end_index + 3])
teams_collecting = ['calvin', 'kalamazoo', 'hope']

#list to keep track of games already collected
#formatted "<home_team>-<away_team>"
games_collected = []

for site in website_list:
    if not "adrianbulldogs" in site:
        schedule_page = site + '/sports/msoc/2017-18/schedule'
    else:
        schedule_page = site + '/sports/m-soccer/2017-18/schedule'
    print("Making request for: " + schedule_page)
    html_schedule_page = urllib2.urlopen(schedule_page)
    schedule_soup = BeautifulSoup(html_schedule_page, "html.parser")
    game_links = schedule_soup.find_all("a", href=re.compile("boxscores"))

    for game_link in game_links:
        game_page = site + game_link['href']
        html_page = urllib2.urlopen(game_page)
        soup = BeautifulSoup(html_page, "html.parser")

        #This collects the scoring summaries
        stats_box = soup.find( "div", { "class" : "stats-box half scoring-summary clearfix"})
        if stats_box is None:
            continue
        table = stats_box.find("tbody")
        data = table.find_all("tr")
        game_header = soup.find( "div", { "class" : "head"})
        game_info = game_header.find("h1")
        current_game = Game(game_info)
        
        if current_game.getGameString() in games_collected:
            continue
        
        games_collected.append(current_game.getGameString())

        #Check if the game is already in the database, if so, move on
        if current_game.isInDatabase():
            continue

        for element in data:
            current_game.addEvent(Event(current_game.getNewId(), element))

        #This collects the starting lineup strings
        starter_strings = []
        logs = soup.findAll("tr", { "class" : "row" })
        for log in logs:
            if checkForHalfTime(log):
                starter_strings.append(log.find("td", { "class" : "play" }).contents[0])

        #send game to DB here
        current_game.sendToDatabase()

        #This collects the game stats (goals and assists)
        collectPlayerGameData(soup, "stats-box half lineup h clearfix", current_game.getHomeTeam(), current_game.getNewId(), starter_strings)
        collectPlayerGameData(soup, "stats-box half lineup v clearfix", current_game.getVisitingTeam(), current_game.getNewId(), starter_strings)
