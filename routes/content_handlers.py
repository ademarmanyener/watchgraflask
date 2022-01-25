# -*- encoding: utf-8 -*-
from includes import *

@app.route('/<title_url>')
def content_redirect(title_url):
  if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

  select_content = content.query.filter_by(titleUrl=title_url).first()
  if select_content == None: return redirect(url_for('home'))

  if select_content.type == 'MOVIE':
    # check player 
    if len(moviePlayer.query.filter(and_(moviePlayer.idContent == select_content.idContent, moviePlayer.visibility == True)).all()) >= 1:
      return redirect(url_for('movie_watch', title_url=select_content.titleUrl))
    else:
      return error(err_msg='Bu film için oynatıcılar siteye henüz yüklenmedi.', ret_url=url_for('home'))

  elif select_content.type == 'TV':
    # check season
    if len(tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == select_content.idContent, tvSeasonContent.visibility == True)).all()) >= 1:
      return redirect(url_for('tv_title', title_url=select_content.titleUrl))
    else:
      return error(err_msg='Bu dizi için sezonlar henüz siteye yüklenmedi.', ret_url=url_for('home'))
  
  return redirect(url_for('home'))