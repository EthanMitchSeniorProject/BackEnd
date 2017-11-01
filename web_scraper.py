# Necessary imports for the Player classes and for the web_scraping library
import urllib.request as urllib2
from bs4 import BeautifulSoup
from Soccer.soccer_player import SoccerPlayer
from Volleyball.volleyball_player import VolleyballPlayer

# Men's Soccer team statistics sites
calvin_page = {'team_name' : 'Calvin', 'site' : 'http://calvinknights.com/sports/msoc/2017-18/teams/calvin?view=profile&r=0&pos=kickers'}
hope_page = {'team_name' : 'Hope', 'site' : 'http://athletics.hope.edu/sports/msoc/2017-18/teams/hope?view=profile&r=0&pos=kickers'}
kalamazoo_page = {'team_name' : 'Kalamazoo', 'site' : 'http://hornets.kzoo.edu/sports/msoc/2017-18/teams/kalamazoo?view=profile&r=0&pos=kickers'}
adrian_page = {'team_name' : 'Adrian', 'site' : 'http://www.adrianbulldogs.com/sports/m-soccer/2017-18/teams/adrian?view=profile&r=0&pos=kickers'}
albion_page = {'team_name' : 'Albion', 'site' : 'http://www.gobrits.com/sports/msoc/2017-18/teams/albion?view=profile&r=0&pos=kickers'}
alma_page = {'team_name' : 'Alma', 'site' : 'http://almascots.com/sports/msoc/2017-18/teams/alma?view=profile&r=0&pos=kickers'}
olivet_page = {'team_name' : 'Olivet', 'site' : 'http://www.olivetcomets.com/sports/msoc/2017-18/teams/olivet?view=profile&r=0&pos=kickers'}
trine_page = {'team_name' : 'Trine', 'site' : 'http://www.trinethunder.com/sports/msoc/2017-18/teams/trine?view=profile&r=0&pos=kickers'}

# Women's Volleyball team statistics sites
calvin_vball_page = {'team_name' : 'Calvin', 'site' : 'http://calvinknights.com/sports/wvball/2017-18/teams/calvin?view=profile&r=0&pos='}
hope_vball_page = {'team_name' : 'Hope', 'site': 'http://athletics.hope.edu/sports/wvball/2017-18/teams/hope?view=profile&r=0&pos='}
kalamazoo_vball_page = {'team_name' : 'Kalamazoo', 'site' : 'http://hornets.kzoo.edu/sports/wvball/2017-18/teams/kalamazoo?view=profile&r=0&pos='}
adrian_vball_page = {'team_name' : 'Adrian', 'site' : 'http://www.adrianbulldogs.com/sports/w-volley/2017-18/teams/adrian?view=profile&r=0&pos='}
albion_vball_page = {'team_name' : 'Albion', 'site' : 'http://www.gobrits.com/sports/wvball/2017-18/teams/albion?view=profile&r=0&pos='}
alma_vball_page = {'team_name' : 'Alma', 'site' : 'http://almascots.com/sports/wvball/2017-18/teams/alma?view=profile&r=0&pos='}
olivet_vball_page = {'team_name' : 'Olivet', 'site' : 'http://www.olivetcomets.com/sports/wvball/2017-18/teams/olivet?view=profile&r=0&pos='}
trine_vball_page = {'team_name' : 'Trine', 'site' : 'http://www.trinethunder.com/sports/wvball/2017-18/teams/trine?view=profile&r=0&pos='}

# Add the team sites to a list to be able to loop through
website_list = (calvin_vball_page, hope_vball_page, kalamazoo_vball_page, adrian_vball_page, albion_vball_page,
    alma_vball_page, olivet_vball_page, trine_vball_page, calvin_page, hope_page, kalamazoo_page, adrian_page,
    albion_page, alma_page, olivet_page, trine_page)

# Loop through each site
for page in website_list:

    html_page = urllib2.urlopen(page['site'])
    soup = BeautifulSoup(html_page, "html.parser")

    # Only search through the main statistics table, this query is more selective so we get fewer results
    # Check if it is a men's soccer link or a women's volleyball link
    if "msoc" in page['site'] or "m-soccer" in page['site']:
        tab_panel = soup.find("div", { "class" : "tab-panel clearfix active "})
        stats_box = tab_panel.find( "div", { "class" : "stats-box stats-box-alternate full clearfix"})

    if "wvball" in page['site'] or "w-volley" in page['site']:
        # Check if it is Trine's site because they have the same exact html tag in two different locations
        if "trine" in page['site']:
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
            if "msoc" in page['site'] or "m-soccer" in page['site']:
                temp_player = SoccerPlayer(element, page['team_name'])
                temp_player.sendToDatabase()
            if "wvball" in page['site'] or "w-volley" in page['site']:
                temp_player = VolleyballPlayer(element, page['team_name'])
                temp_player.sendToDatabase()