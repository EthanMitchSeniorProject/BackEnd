# Necessary imports for the Player classes and for the web_scraping library
import urllib.request as urllib2
import requests
import json
from bs4 import BeautifulSoup
from Soccer.soccer_player import SoccerPlayer
from Volleyball.volleyball_player import VolleyballPlayer

# Add the team sites to a list to be able to loop through
soccer_pages = json.loads(requests.get("http://localhost:3000/soccer/teams").text)
vball_pages = json.loads(requests.get("http://localhost:3000/vball/teams").text)

website_list = []

for page in soccer_pages:
    website_list.append(page)

for page in vball_pages:
    website_list.append(page)

# Loop through each site
for page in website_list:
    html_page = urllib2.urlopen(page['url_route'])
    soup = BeautifulSoup(html_page, "html.parser")

    # Only search through the main statistics table, this query is more selective so we get fewer results
    # Check if it is a men's soccer link or a women's volleyball link
    if "msoc" in page['url_route'] or "m-soccer" in page['url_route']:
        tab_panel = soup.find("div", { "class" : "tab-panel clearfix active "})
        stats_box = tab_panel.find( "div", { "class" : "stats-box stats-box-alternate full clearfix"})

    if "wvball" in page['url_route'] or "w-volley" in page['url_route']:
        # Check if it is Trine's site because they have the same exact html tag in two different locations
        if "trine" in page['url_route']:
            all = soup.findAll("div", { "class" : "stats-box stats-box-alternate full clearfix"})
            stats_box = all[1]
        else:
            stats_box = soup.find("div", { "class" : "stats-box stats-box-alternate full clearfix"})

    # Sort through the table
    table = stats_box.find("table")

    # Loop through each row in the table
    for element in table:
        href = element.find("a")

        # If href contains "players" it is a player stat table, need to parse the data
        if "players" in str(href):

            # Again check if it is a men's soccer link or a women's volleyball link
            if "msoc" in page['url_route'] or "m-soccer" in page['url_route']:
                temp_player = SoccerPlayer(element, page['school_name'])
                temp_player.sendToDatabase()
            if "wvball" in page['url_route'] or "w-volley" in page['url_route']:
                temp_player = VolleyballPlayer(element, page['school_name'])
                temp_player.sendToDatabase()