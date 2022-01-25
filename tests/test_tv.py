# -*- encoding: utf-8 -*-
from includes import *
from tmdbv3api import TV 
from tmdbv3api import Season

tv = TV()
season = Season()

SHOW_ID = 1399

os.system('clear')
def main():
  for get_season in tv.details(show_id=SHOW_ID).seasons:
    print('-> season: ' + str(get_season.name) + ' ' + str(get_season.episode_count) + ' bölüm. ' + str(get_season.season_number))
    for get_episode in season.details(SHOW_ID, get_season.season_number).episodes:
      print('   L-> episode: ' + str(get_episode.name) + ' ' + str(get_episode.episode_number))

main()