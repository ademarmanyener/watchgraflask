# -*- encoding: utf-8 -*-
from includes import *

"""
ajax codes for all kind of users
"""

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

###########################
###### content->seasons
###########################
@app.route('/mainproc/content/seasons', methods=['POST'])
def mainproc_content_seasons():
  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # SELECT FIRST PLAYER
  if get_function == 'selectFirstPlayer':
    content_id = request.get_json()['idContent']
    tv_season_id = request.get_json()['idTvSeason']
    tv_episode_id = request.get_json()['idTvEpisode']

    return make_response(jsonify({'ret_url': url_for('tv_watch', title_url=content.query.filter(and_(content.idContent == content_id, content.type == 'TV')).first().titleUrl, season_number=tvSeasonContent.query.filter(and_(tvSeasonContent.idTvSeason == tv_season_id)).first().seasonNumber, episode_number=tvEpisodeContent.query.filter(and_(tvEpisodeContent.idTvEpisode == tv_episode_id)).first().episodeNumber)}))

  # SELECT RANDOM EPISODE
  if get_function == 'selectRandomEpisode':
    get_content_id = request.get_json()['idContent']

    get_content = content.query.filter(and_(content.idContent == get_content_id, content.type == 'TV')).first()
    if not get_content_id: return make_response(jsonify({'err_msg': 'Bu dizi içeriği bulunamadı.'}))

    get_all_players = tvPlayer.query.filter(tvPlayer.idContent == get_content_id).all()
    if not get_all_players: return make_response(jsonify({'err_msg': 'Bu dizi için uygun bir oynatıcı bulunamadı.'}))

    get_player = random.choice(get_all_players)

    return make_response(jsonify({'ret_url': url_for('tv_watch', title_url=get_content.titleUrl, season_number=get_player.seasonNumber, episode_number=get_player.episodeNumber)}))
###########################
###### end content->seasons
###########################

######################################################################################################
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
# ************************************************************************************************** #
######################################################################################################

###########################
###### content->season->episodes
###########################
@app.route('/mainproc/content/season/episodes', methods=['POST'])
def mainproc_content_season_episodes():
  if not request.is_json: return make_response(jsonify({'err_msg': '`JSON` geçersiz.'}))

  get_function = request.get_json()['function']
  if not get_function: return make_response(jsonify({'err_msg': '`Function` boş bırakıldı.'}))

  # SELECT PREVIOUS EPISODE
  if get_function == 'selectPreviousEpisode':
    try:
      content_id = request.get_json()['idContent']
      tv_season_id = request.get_json()['idTvSeason']
      tv_episode_id = request.get_json()['idTvEpisode']

      ep = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == content_id, tvEpisodeContent.idTvSeason == tv_season_id, tvEpisodeContent.idTvEpisode == tv_episode_id)).first()
      if not ep:
        return make_response(jsonify({'err_msg': 'Could not load the episode.'}))

      previous_ep = ep.get_previous_episode()

      return make_response(jsonify({'ret_url': url_for('tv_watch', title_url=previous_ep.get_content().titleUrl, season_number=previous_ep.get_season().seasonNumber, episode_number=previous_ep.episodeNumber)}))
    except Exception as e:
      return make_response(jsonify({'err_msg': str(e)}))

  # SELECT NEXT EPISODE
  if get_function == 'selectNextEpisode':
    try:
      content_id = request.get_json()['idContent']
      tv_season_id = request.get_json()['idTvSeason']
      tv_episode_id = request.get_json()['idTvEpisode']

      ep = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == content_id, tvEpisodeContent.idTvSeason == tv_season_id, tvEpisodeContent.idTvEpisode == tv_episode_id)).first()
      if not ep:
        return make_response(jsonify({'err_msg': 'Could not load the episode.'}))

      next_ep = ep.get_next_episode()

      return make_response(jsonify({'ret_url': url_for('tv_watch', title_url=next_ep.get_content().titleUrl, season_number=next_ep.get_season().seasonNumber, episode_number=next_ep.episodeNumber)}))
    except Exception as e:
      return make_response(jsonify({'err_msg': str(e)}))
###########################
###### end content->season->episodes
###########################
