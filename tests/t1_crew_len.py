# -*- encoding: utf-8 -*-
from includes import *

# TODO: max get 20 cast

DEF_TMDB_ID = 550
DEF_MAX_LIST = 20

def main():
  get_casts = tmdb.Movies(DEF_TMDB_ID).credits()['cast']

  for loop_i in range(DEF_MAX_LIST):
    print(' ==> {} {}'.format(loop_i, len(get_casts)))
    if loop_i < len(get_casts):
      print(' -> {}'.format(get_casts[loop_i]))

main()