import urllib.request as urllib2
from bs4 import BeautifulSoup
from Game.Event import Event
from Game.Game import Game

calvin_game_page = 'http://calvinknights.com/sports/msoc/2017-18/boxscores/20170901_d3xv.xml'

html_page = urllib2.urlopen(calvin_game_page)
soup = BeautifulSoup(html_page, "html.parser")
stats_box = soup.find( "div", { "class" : "stats-box half scoring-summary clearfix"})
table = stats_box.find("tbody")
data = table.find_all("tr")
for element in data:
    #print(element)
    temp_event = Event(element)
game_header = soup.find( "div", { "class" : "head"})
game_info = game_header.find("h1")
temp_game = Game(game_info)