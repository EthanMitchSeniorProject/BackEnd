import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
from Soccer.Game.event import Event
from Soccer.Game.game import Game

#This method takes in a beautiful soup element
#and checks to see if the time stamp is at half-time.
#If so, this will contain the starting lineup information
#Verified with Calvin, Kzoo, Hope, Tufts, etc. 
def checkForHalfTime(log_element):
    time = log.find("td", { "class" : "time" })
    return ((time is not None) and (len(time.contents) > 0) and ("45:00" in time.contents[0]))

#schedule page
calvin_schedule_page = 'http://calvinknights.com/sports/msoc/2017-18/schedule'
html_schedule_page = urllib2.urlopen(calvin_schedule_page)
schedule_soup = BeautifulSoup(html_schedule_page, "html.parser")
game_links = schedule_soup.find_all("a", href=re.compile("boxscores"))
for game_link in game_links:
    calvin_game_page = 'http://calvinknights.com' + game_link['href']
    html_page = urllib2.urlopen(calvin_game_page)
    soup = BeautifulSoup(html_page, "html.parser")
    stats_box = soup.find( "div", { "class" : "stats-box half scoring-summary clearfix"})
    if stats_box is None:
        break
    table = stats_box.find("tbody")
    data = table.find_all("tr")
    game_header = soup.find( "div", { "class" : "head"})
    game_info = game_header.find("h1")
    current_game = Game(game_info)
    for element in data:
        print(element)
        current_game.addEvent(Event(element))

    #testing game log parsing
    logs = soup.findAll("tr", { "class" : "row" })
    for log in logs:
        if not checkForHalfTime(log):
            continue
        print(log)
