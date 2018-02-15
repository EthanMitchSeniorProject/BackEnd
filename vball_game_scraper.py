# Necessary imports for the volleyball game web scraper
import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
from Volleyball.Game.game import Game
from Volleyball.Game.event import Event

# Starting url address for the web scraper
calvin_base_page = 'http://calvinknights.com'

# Connect to the schedule page and find all the box score links
schedule_page = calvin_base_page + '/sports/wvball/2017-18/schedule'
html_schedule_page = urllib2.urlopen(schedule_page)
schedule_soup = BeautifulSoup(html_schedule_page, "html.parser")
game_links = schedule_soup.find_all("a", href=re.compile("boxscores"))

# Create two empty lists for use
game_links_list = []
play_by_play_list = []

# For each of the box score game links in the found links
for game_link in game_links:
    
    # Add the extension url onto the starting url
    game_page = calvin_base_page + game_link['href']

    # If the game has already been found or if it is a game we do not want...
    if (game_page in game_links_list or "tournament" in game_page):
        continue

    # Add the game to the list so we don't loop through it again
    game_links_list.append(game_page)

    # Open up the box score page for parsing
    html_page = urllib2.urlopen(game_page)
    soup = BeautifulSoup(html_page, "html.parser")

    # Get the link to the "play-by-play" table
    play_by_play = soup.find("a", href=re.compile("view=plays"))

    # If there is no "play-by-play" table...
    if play_by_play is None:
        continue

    # Add the extension url onto the starting url again
    play_by_play_page = calvin_base_page + play_by_play['href']
    play_by_play_list.append(play_by_play_page)

# Loop through all the "play-by-play" page tables
for play_stats in play_by_play_list:
    
    # Open the "play-by-play" page for parsing
    html_page = urllib2.urlopen(play_stats)
    soup = BeautifulSoup(html_page, "html.parser")

    # Get Game information
    game_info = soup.find("div", {"class" : "align-center"})
    current_game = Game(game_info)

    # Get "play-by-play" records
    stats_box = soup.find_all("div", {"class" : "stats-fullbox clearfix"})
    table = stats_box[1].find("table")
    data = table.find_all("tr")

    previous_event = None

    # Loop through all the "play-by-play" records
    for element in data:

        td_list = element.findAll("td")

        # If the record only has 3 rows...
        if (len(td_list) == 3):
            
            temp_description = td_list[1].contents[0]

            # Only create plays for plays that we want to store...
            # TODO: Rework these two if statements to only be one that checks for "Point"
            if ((temp_description.find("sub") == -1) and (temp_description.find("Timeout") == -1) and (temp_description.find("starters") == -1)):
                
                if (not temp_description.isspace() and (temp_description.find("Point") != -1)):
                    current_event = Event(current_game.getNewId(), current_game.getHomeTeam(), current_game.getAwayTeam(), element, previous_event)
                    current_game.addEvent(current_event)
                    previous_event = current_event
    
    # Send the current game and all its plays to the database
    current_game.sendToDatabase()