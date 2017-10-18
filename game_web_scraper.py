import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
from Soccer.Game.event import Event
from Soccer.Game.game import Game

#Need to create a "already collected" class so that we don't re-collect the same data

#This method takes in a beautiful soup element
#and checks to see if the time stamp is at half-time.
#If so, this will contain the starting lineup information
#Verified with Calvin, Kzoo, Hope, Tufts, etc. 
def checkForHalfTime(log_element):
    time = log.find("td", { "class" : "time" })
    return ((time is not None) and (len(time.contents) > 0) and ("45:00" in time.contents[0]))

#This is a method because the same code is used for both home and away teams
#The table_class_string param specifies which table, home or visiting, to look for
def collectPlayerGameData(soup, table_class_string):
    game_stat_summary = soup.find("div", { "class" : table_class_string})
    player_list = game_stat_summary.findAll("tr")
    for player in player_list:
        player_name = player.find("a", { "class" : "player-name"})
        if (player_name is None):
            player_name = player.find("span", { "class" : "player-name"})
        player_stats = player.findAll("td")
        if (len(player_stats) == 0) or (player_name is None) or ("TEAM" in player_name):
            continue
        #0 - Shots
        #1 - Shots on Goal
        #2 - Goals
        #3 - Assists
        print(player_name.contents[0])
        print(player_stats[2].contents[0])
        print(player_stats[3].contents[0])


#schedule page
calvin_schedule_page = 'http://calvinknights.com/sports/msoc/2017-18/schedule'
html_schedule_page = urllib2.urlopen(calvin_schedule_page)
schedule_soup = BeautifulSoup(html_schedule_page, "html.parser")
game_links = schedule_soup.find_all("a", href=re.compile("boxscores"))
for game_link in game_links:
    calvin_game_page = 'http://calvinknights.com' + game_link['href']
    html_page = urllib2.urlopen(calvin_game_page)
    soup = BeautifulSoup(html_page, "html.parser")

    #This collects the scoring summaries
    stats_box = soup.find( "div", { "class" : "stats-box half scoring-summary clearfix"})
    if stats_box is None:
        break
    table = stats_box.find("tbody")
    data = table.find_all("tr")
    game_header = soup.find( "div", { "class" : "head"})
    game_info = game_header.find("h1")
    current_game = Game(game_info)
    for element in data:
        current_game.addEvent(Event(element))

    #This collects the starting lineup strings
    logs = soup.findAll("tr", { "class" : "row" })
    for log in logs:
        if not checkForHalfTime(log):
            continue
        print(log)

    #This collects the game stats (goals and assists)
    collectPlayerGameData(soup, "stats-box half lineup h clearfix")
    collectPlayerGameData(soup, "stats-box half lineup v clearfix")
