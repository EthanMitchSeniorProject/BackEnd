import urllib.request as urllib2
from bs4 import BeautifulSoup

calvin_page = 'http://calvinknights.com/sports/msoc/2017-18/teams/calvin?view=profile&r=0&pos=kickers'

html_page = urllib2.urlopen(calvin_page)
soup = BeautifulSoup(html_page, "html.parser")
#Only search through the main statistics table, this query is more selective so we get fewer results
tab_panel = soup.find("div", { "class" : "tab-panel clearfix active "})
stats_box = tab_panel.find( "div", { "class" : "stats-box stats-box-alternate full clearfix"})

#sort through the table
table = stats_box.find("table")
for element in table:
    href = element.find("a")
    #if href contains "players" it is a player stat table, need to parse the data
    if "players" in str(href):
        print(element)
        print('---------------------')
        #This is where we will send in the html elements to a Player constructor where the data will be parsed