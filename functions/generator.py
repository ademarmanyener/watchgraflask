# -*- encoding: utf-8 -*-
from includes import *

"""
// generator
"""

def id_generator(size=24, title='', chars=string.ascii_letters + string.digits):
  current_year_without_century = time.strftime('%y')
  random_character = ''.join(random.choice(chars) for _ in range(size))
  if title == '': return str(random_character) + str(current_year_without_century)
  else: return str(title) + str(current_year_without_century) + str(random_character)