# -*- encoding: utf-8 -*-
from includes import *
from tmdbv3api import Movie 

movie = Movie()

SHOW_ID = 120 

os.system('clear')
def main():
    print('===== %r =======' % movie.details(SHOW_ID).title)
    for get_genre in movie.details(SHOW_ID).genres:
        print(' ==> (%r), %r' % (str(get_genre.id), get_genre.name))

main()