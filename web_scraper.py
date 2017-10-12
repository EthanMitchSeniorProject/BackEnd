import urllib.request as urllib2
from bs4 import BeautifulSoup
from Soccer.SoccerPlayer import SoccerPlayer
from Volleyball.VolleyballPlayer import VolleyballPlayer

calvin_page = 'http://calvinknights.com/sports/msoc/2017-18/teams/calvin?view=profile&r=0&pos=kickers'
hope_page = 'http://athletics.hope.edu/sports/msoc/2017-18/teams/hope?view=profile&r=0&pos=kickers'
kalamazoo_page = 'http://hornets.kzoo.edu/sports/msoc/2017-18/teams/kalamazoo?view=profile&r=0&pos=kickers'

calvin_vball_page = 'http://calvinknights.com/sports/wvball/2017-18/teams/calvin?view=profile&r=0&pos='
hope_vball_page = 'http://athletics.hope.edu/sports/wvball/2017-18/teams/hope?view=profile&r=0&pos='
kalamazoo_vball_page = 'http://hornets.kzoo.edu/sports/wvball/2017-18/teams/kalamazoo?view=profile&r=0&pos='

website_list = (calvin_vball_page, hope_vball_page, kalamazoo_vball_page, calvin_page, hope_page, kalamazoo_page)

for site in website_list:
    html_page = urllib2.urlopen(site)
    soup = BeautifulSoup(html_page, "html.parser")
    #Only search through the main statistics table, this query is more selective so we get fewer results
    if "msoc" in site:
        tab_panel = soup.find("div", { "class" : "tab-panel clearfix active "})
        stats_box = tab_panel.find( "div", { "class" : "stats-box stats-box-alternate full clearfix"})
    if "wvball" in site:
        stats_box = soup.find("div", { "class" : "stats-box stats-box-alternate full clearfix"})

    #sort through the table
    table = stats_box.find("table")
    for element in table:
        href = element.find("a")
        #if href contains "players" it is a player stat table, need to parse the data
        if "players" in str(href):
            #print(element)
            #This is where we will send in the html elements to a Player constructor where the data will be parsed
            if "msoc" in site:
                temp_player = SoccerPlayer(element)
            if "wvball" in site:
                temp_player = VolleyballPlayer(element)