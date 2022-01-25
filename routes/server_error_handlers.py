# -*- encoding: utf-8 -*-
from includes import *

background_gifs_list = [
  'http://www.reactiongifs.us/wp-content/uploads/2015/04/nothing_to_see_here_naked_gun.gif',
  'https://media.giphy.com/media/NTur7XlVDUdqM/giphy.gif',
  'https://media.giphy.com/media/QZehD8CLv2JfG/giphy.gif',
  'https://media.giphy.com/media/l3q2xkbanZlsiPqIE/giphy.gif',
  'https://media.giphy.com/media/aX2P8kEFqt8u4/giphy.gif',
  'https://media.giphy.com/media/nrXif9YExO9EI/giphy.gif',
]

@app.errorhandler(404)
def not_found(self):
  """Page not found."""
  return render_template('error/404.html', header=False, footer=False, background_gif_src=random.choice(background_gifs_list))

@app.errorhandler(400)
def bad_request(self):
  """Bad request."""
  return error(err_msg='400 - Kötü İstek :( {}'.format(self), ret_url=url_for('home'))

@app.errorhandler(500)
def server_error(self):
  """Internal server error."""
  try: print('e')
  except Exception as e: return 'e'
  return error(err_msg='500 - Sunucu Hatası :( {}'.format(self), ret_url=url_for('home'))