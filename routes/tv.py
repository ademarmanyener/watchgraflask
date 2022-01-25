# -*- encoding: utf-8 -*-
from includes import *

@app.route('/tv/func/<function>/proc', methods=['POST'])
def tv_title_func_proc(function):
  if request.is_json == False: return error(err_msg='JSON değil.')

  if function == 'send_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_text = request.get_json()['text']
    get_contains_spoiler = request.get_json()['contains_spoiler']

    SELECTED_SPOILER = 0
    if get_contains_spoiler: SELECTED_SPOILER = 1

    if get_text:
      db.session.add(tvTitleComment(
        idContent = get_content_id,
        idTvSeason = get_tv_season_id,
        idAddProfile = session['PROFILE']['idProfile'],
        idAddAccount = session['ACCOUNT']['idAccount'],
        text = get_text,
        replyTo = '',
        visibility = 1,
        spoiler = SELECTED_SPOILER,
        lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
      ))
      db.session.commit()

      latest_comment =  tvTitleComment.query.filter(and_(tvTitleComment.idContent == get_content_id, tvTitleComment.idTvSeason == get_tv_season_id, tvTitleComment.replyTo == '', tvTitleComment.idAddProfile == session['PROFILE']['idProfile'], tvTitleComment.idAddAccount == session['ACCOUNT']['idAccount'])).order_by(tvTitleComment.addDate.desc()).first()
      if latest_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

      return make_response(jsonify({'succ_msg': 'Yorumunuz başarıyla gönderildi!', \
                                    'latest_comment_id': latest_comment.idComment, \
                                    'latest_comment_text': latest_comment.text, \
                                    }))
    else: return make_response(jsonify({'err_msg': 'Boş yorum yapılamaz.'}))

  if function == 'send_reply':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_reply = request.get_json()['reply']
    get_reply_to = request.get_json()['replyTo']

    if get_reply and get_reply_to:
      if tvTitleComment.query.filter_by(idComment=get_reply_to).first() == None: return make_response(jsonify({'err_msg': 'Olmayan bir yoruma mı yanıt göndericeksin?'}))

      db.session.add(tvTitleComment(
        idContent = get_content_id,
        idTvSeason = get_tv_season_id,
        idAddProfile = session['PROFILE']['idProfile'],
        idAddAccount = session['ACCOUNT']['idAccount'],
        text = get_reply,
        replyTo = get_reply_to,
        visibility = 1,
        spoiler = 0,
        lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
      ))
      db.session.commit()

      latest_reply =  tvTitleComment.query.filter(and_(tvTitleComment.idContent == get_content_id, tvTitleComment.idTvSeason == get_tv_season_id, tvTitleComment.replyTo != '', tvTitleComment.idAddProfile == session['PROFILE']['idProfile'], tvTitleComment.idAddAccount == session['ACCOUNT']['idAccount'])).order_by(tvTitleComment.addDate.desc()).first()
      if latest_reply == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

      return make_response(jsonify({'succ_msg': 'Yanıtınız başarıyla gönderildi!', \
                                    'latest_reply_id': latest_reply.idComment, \
                                    'latest_reply_text': latest_reply.text, \
                                    'latest_reply_replyto': latest_reply.replyTo, \
                                    }))
    else: return make_response(jsonify({'err_msg': 'Boş yanıt yapılamaz.'}))

  if function == 'select_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_comment_id = request.get_json()['idComment']

    get_comment = tvTitleComment.query.filter(and_(tvTitleComment.idContent == get_content_id, tvTitleComment.idTvSeason == get_tv_season_id, tvTitleComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    return make_response(jsonify({'succ_msg': 'YES', \
                                  'selected_comment_text': get_comment.text, \
                                  }))

  if function == 'delete_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_comment_id = request.get_json()['idComment']

    get_comment = tvTitleComment.query.filter(and_(tvTitleComment.idContent == get_content_id, tvTitleComment.idTvSeason == get_tv_season_id, tvTitleComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))
    if get_comment.idAddProfile == session['PROFILE']['idProfile'] and get_comment.idAddAccount == session['ACCOUNT']['idAccount']: pass
    else: return make_response(jsonify({'err_msg': 'Bu yorumun sizin profilinize ait olduğuna emin misiniz?'}))

    get_comment.drop()

    return make_response(jsonify({'succ_msg': 'Yorumunuz başarıyla silindi!', 'deleted_comment_id': get_comment.idComment}))

  if function == 'like_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_comment_id = request.get_json()['idComment']

    get_comment = tvTitleComment.query.filter(and_(tvTitleComment.idContent == get_content_id, tvTitleComment.idTvSeason == get_tv_season_id, tvTitleComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    get_comment_rate = tvTitleCommentRate.query.filter(and_(tvTitleCommentRate.idContent == get_content_id, tvTitleCommentRate.idTvSeason == get_tv_season_id, tvTitleCommentRate.idComment == get_comment_id, tvTitleCommentRate.idRateProfile == session['PROFILE']['idProfile'], tvTitleCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], tvTitleCommentRate.rateType == 'LIKE')).first()
    if get_comment_rate == None:
      if get_comment.idAddAccount == session['ACCOUNT']['idAccount'] and get_comment.idAddProfile == session['PROFILE']['idProfile']:
        return make_response(jsonify({'err_msg': 'Kendi profiliniz tarafından yapılan yorumları beğenemezsiniz.'}))
      else:
        db.session.add(tvTitleCommentRate(
          idContent = get_content_id,
          idTvSeason = get_tv_season_id,
          idComment = get_comment_id,
          idRateProfile = session['PROFILE']['idProfile'],
          idRateAccount = session['ACCOUNT']['idAccount'],
          rateType = 'LIKE',
        ))
        db.session.commit()

        # if the profile has disliked the comment, then drop it first
        select_dislike = tvTitleCommentRate.query.filter(and_(tvTitleCommentRate.idContent == get_content_id, tvTitleCommentRate.idTvSeason == get_tv_season_id, tvTitleCommentRate.idComment == get_comment_id, tvTitleCommentRate.idRateProfile == session['PROFILE']['idProfile'], tvTitleCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], tvTitleCommentRate.rateType == 'DISLIKE')).first()
        if select_dislike:
          select_dislike.drop()
          return make_response(jsonify({'gave_like': 'Yorumu başarıyla beğendiniz!', 'took_dislike': 'OK'}))

        return make_response(jsonify({'gave_like': 'Yorumu başarıyla beğendiniz!'}))
    else:
      get_comment_rate.drop()
      return make_response(jsonify({'took_like': 'Beğeniyi geri aldınız.'}))

  if function == 'dislike_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_comment_id = request.get_json()['idComment']

    get_comment = tvTitleComment.query.filter(and_(tvTitleComment.idContent == get_content_id, tvTitleComment.idTvSeason == get_tv_season_id, tvTitleComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    get_comment_rate = tvTitleCommentRate.query.filter(and_(tvTitleCommentRate.idContent == get_content_id, tvTitleCommentRate.idTvSeason == get_tv_season_id, tvTitleCommentRate.idComment == get_comment_id, tvTitleCommentRate.idRateProfile == session['PROFILE']['idProfile'], tvTitleCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], tvTitleCommentRate.rateType == 'DISLIKE')).first()
    if get_comment_rate == None:
      if get_comment.idAddAccount == session['ACCOUNT']['idAccount'] and get_comment.idAddProfile == session['PROFILE']['idProfile']:
        return make_response(jsonify({'err_msg': 'Kendi profiliniz tarafından yapılan yorumlara dislike atamazsın.'}))
      else:
        db.session.add(tvTitleCommentRate(
          idContent = get_content_id,
          idTvSeason = get_tv_season_id,
          idComment = get_comment_id,
          idRateProfile = session['PROFILE']['idProfile'],
          idRateAccount = session['ACCOUNT']['idAccount'],
          rateType = 'DISLIKE',
        ))
        db.session.commit()

        # if the profile has liked the comment, then drop it first
        select_like = tvTitleCommentRate.query.filter(and_(tvTitleCommentRate.idContent == get_content_id, tvTitleCommentRate.idTvSeason == get_tv_season_id, tvTitleCommentRate.idComment == get_comment_id, tvTitleCommentRate.idRateProfile == session['PROFILE']['idProfile'], tvTitleCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], tvTitleCommentRate.rateType == 'LIKE')).first()
        if select_like:
          select_like.drop()
          return make_response(jsonify({'gave_dislike': 'Başarıyla dislikledınız!', 'took_like': 'OK'}))

        return make_response(jsonify({'gave_dislike': 'Başarıyla dislikledınız!'}))
    else:
      get_comment_rate.drop()
      return make_response(jsonify({'took_dislike': 'Dislikeyi geri aldınız.'}))

@app.route('/tv/watch/func/<function>/proc', methods=['POST'])
def tv_watch_func_proc(function):
  if request.is_json == False: return error(err_msg='JSON değil.')

  if function == 'send_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_tv_episode_id = request.get_json()['idTvEpisode']
    get_text = request.get_json()['text']
    get_contains_spoiler = request.get_json()['contains_spoiler']

    SELECTED_SPOILER = 0
    if get_contains_spoiler: SELECTED_SPOILER = 1

    if get_text:
      db.session.add(tvComment(
        idContent = get_content_id,
        idTvSeason = get_tv_season_id,
        idTvEpisode = get_tv_episode_id,
        idAddProfile = session['PROFILE']['idProfile'],
        idAddAccount = session['ACCOUNT']['idAccount'],
        text = get_text,
        replyTo = '',
        visibility = 1,
        spoiler = SELECTED_SPOILER,
        lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
      ))
      db.session.commit()

      latest_comment =  tvComment.query.filter(and_(tvComment.idContent == get_content_id, tvComment.idTvSeason == get_tv_season_id, tvComment.idTvEpisode == get_tv_episode_id, tvComment.replyTo == '', tvComment.idAddProfile == session['PROFILE']['idProfile'], tvComment.idAddAccount == session['ACCOUNT']['idAccount'])).order_by(tvComment.addDate.desc()).first()
      if latest_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

      return make_response(jsonify({'succ_msg': 'Yorumunuz başarıyla gönderildi!', \
                                    'latest_comment_id': latest_comment.idComment, \
                                    'latest_comment_text': latest_comment.text, \
                                    }))
    else: return make_response(jsonify({'err_msg': 'Boş yorum yapılamaz.'}))

  if function == 'send_reply':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_tv_episode_id = request.get_json()['idTvEpisode']

    get_reply = request.get_json()['reply']
    get_reply_to = request.get_json()['replyTo']

    if get_reply and get_reply_to:
      if tvComment.query.filter_by(idComment=get_reply_to).first() == None: return make_response(jsonify({'err_msg': 'Olmayan bir yoruma mı yanıt göndericeksin?'}))

      db.session.add(tvComment(
        idContent = get_content_id,
        idTvSeason = get_tv_season_id,
        idTvEpisode = get_tv_episode_id,
        idAddProfile = session['PROFILE']['idProfile'],
        idAddAccount = session['ACCOUNT']['idAccount'],
        text = get_reply,
        replyTo = get_reply_to,
        visibility = 1,
        spoiler = 0,
        lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
      ))
      db.session.commit()

      latest_reply =  tvComment.query.filter(and_(tvComment.idContent == get_content_id, tvComment.idTvSeason == get_tv_season_id, tvComment.idTvEpisode == get_tv_episode_id, tvComment.replyTo != '', tvComment.idAddProfile == session['PROFILE']['idProfile'], tvComment.idAddAccount == session['ACCOUNT']['idAccount'])).order_by(tvComment.addDate.desc()).first()
      if latest_reply == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

      return make_response(jsonify({'succ_msg': 'Yanıtınız başarıyla gönderildi!', \
                                    'latest_reply_id': latest_reply.idComment, \
                                    'latest_reply_text': latest_reply.text, \
                                    'latest_reply_replyto': latest_reply.replyTo, \
                                    }))
    else: return make_response(jsonify({'err_msg': 'Boş yanıt yapılamaz.'}))

  if function == 'select_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_tv_episode_id = request.get_json()['idTvEpisode']
    get_comment_id = request.get_json()['idComment']

    get_comment = tvComment.query.filter(and_(tvComment.idContent == get_content_id, tvComment.idTvSeason == get_tv_season_id, tvComment.idTvEpisode == get_tv_episode_id, tvComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    return make_response(jsonify({'succ_msg': 'YES', \
                                  'selected_comment_text': get_comment.text, \
                                  }))

  if function == 'delete_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_tv_episode_id = request.get_json()['idTvEpisode']
    get_comment_id = request.get_json()['idComment']

    get_comment = tvComment.query.filter(and_(tvComment.idContent == get_content_id, tvComment.idTvSeason == get_tv_season_id, tvComment.idTvEpisode == get_tv_episode_id, tvComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))
    if get_comment.idAddProfile == session['PROFILE']['idProfile'] and get_comment.idAddAccount == session['ACCOUNT']['idAccount']: pass
    else: return make_response(jsonify({'err_msg': 'Bu yorumun sizin profilinize ait olduğuna emin misiniz?'}))

    get_comment.drop()

    return make_response(jsonify({'succ_msg': 'Yorumunuz başarıyla silindi!', 'deleted_comment_id': get_comment.idComment}))

  if function == 'like_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_tv_episode_id = request.get_json()['idTvEpisode']
    get_comment_id = request.get_json()['idComment']

    get_comment = tvComment.query.filter(and_(tvComment.idContent == get_content_id, tvComment.idTvSeason == get_tv_season_id, tvComment.idTvEpisode == get_tv_episode_id, tvComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    get_comment_rate = tvCommentRate.query.filter(and_(tvCommentRate.idContent == get_content_id, tvCommentRate.idTvSeason == get_tv_season_id, tvCommentRate.idTvEpisode == get_tv_episode_id, tvCommentRate.idComment == get_comment_id, tvCommentRate.idRateProfile == session['PROFILE']['idProfile'], tvCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], tvCommentRate.rateType == 'LIKE')).first()
    if get_comment_rate == None:
      if get_comment.idAddAccount == session['ACCOUNT']['idAccount'] and get_comment.idAddProfile == session['PROFILE']['idProfile']:
        return make_response(jsonify({'err_msg': 'Kendi profiliniz tarafından yapılan yorumları beğenemezsiniz.'}))
      else:
        db.session.add(tvCommentRate(
          idContent = get_content_id,
          idTvSeason = get_tv_season_id,
          idTvEpisode = get_tv_episode_id,
          idComment = get_comment_id,
          idRateProfile = session['PROFILE']['idProfile'],
          idRateAccount = session['ACCOUNT']['idAccount'],
          rateType = 'LIKE',
        ))
        db.session.commit()

        # if the profile has disliked the comment, then drop it first
        select_dislike = tvCommentRate.query.filter(and_(tvCommentRate.idContent == get_content_id, tvCommentRate.idTvSeason == get_tv_season_id, tvCommentRate.idTvEpisode == get_tv_episode_id, tvCommentRate.idComment == get_comment_id, tvCommentRate.idRateProfile == session['PROFILE']['idProfile'], tvCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], tvCommentRate.rateType == 'DISLIKE')).first()
        if select_dislike:
          select_dislike.drop()
          return make_response(jsonify({'gave_like': 'Yorumu başarıyla beğendiniz!', 'took_dislike': 'OK'}))

        return make_response(jsonify({'gave_like': 'Yorumu başarıyla beğendiniz!'}))
    else:
      get_comment_rate.drop()
      return make_response(jsonify({'took_like': 'Beğeniyi geri aldınız.'}))

  if function == 'dislike_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_tv_season_id = request.get_json()['idTvSeason']
    get_tv_episode_id = request.get_json()['idTvEpisode']
    get_comment_id = request.get_json()['idComment']

    get_comment = tvComment.query.filter(and_(tvComment.idContent == get_content_id, tvComment.idTvSeason == get_tv_season_id, tvComment.idTvEpisode == get_tv_episode_id, tvComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    get_comment_rate = tvCommentRate.query.filter(and_(tvCommentRate.idContent == get_content_id, tvCommentRate.idTvSeason == get_tv_season_id, tvCommentRate.idTvEpisode == get_tv_episode_id, tvCommentRate.idComment == get_comment_id, tvCommentRate.idRateProfile == session['PROFILE']['idProfile'], tvCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], tvCommentRate.rateType == 'DISLIKE')).first()
    if get_comment_rate == None:
      if get_comment.idAddAccount == session['ACCOUNT']['idAccount'] and get_comment.idAddProfile == session['PROFILE']['idProfile']:
        return make_response(jsonify({'err_msg': 'Kendi profiliniz tarafından yapılan yorumlara dislike atamazsın.'}))
      else:
        db.session.add(tvCommentRate(
          idContent = get_content_id,
          idTvSeason = get_tv_season_id,
          idTvEpisode = get_tv_episode_id,
          idComment = get_comment_id,
          idRateProfile = session['PROFILE']['idProfile'],
          idRateAccount = session['ACCOUNT']['idAccount'],
          rateType = 'DISLIKE',
        ))
        db.session.commit()

        # if the profile has liked the comment, then drop it first
        select_like = tvCommentRate.query.filter(and_(tvCommentRate.idContent == get_content_id, tvCommentRate.idTvSeason == get_tv_season_id, tvCommentRate.idTvEpisode == get_tv_episode_id, tvCommentRate.idComment == get_comment_id, tvCommentRate.idRateProfile == session['PROFILE']['idProfile'], tvCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], tvCommentRate.rateType == 'LIKE')).first()
        if select_like:
          select_like.drop()
          return make_response(jsonify({'gave_dislike': 'Başarıyla dislikledınız!', 'took_like': 'OK'}))

        return make_response(jsonify({'gave_dislike': 'Başarıyla dislikledınız!'}))
    else:
      get_comment_rate.drop()
      return make_response(jsonify({'took_dislike': 'Dislikeyi geri aldınız.'}))

###################
#
# this page finds the lowest season number
# of the content and redirects
#
###################
@app.route('/tv/<title_url>', methods=['POST', 'GET'])
@app.route('/dizi/<title_url>', methods=['POST', 'GET'])
def tv_title(title_url):
  if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

  select_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'TV')).first()
  if select_content == None: return error(err_msg='Bu içerik bulunamadı.', ret_url=url_for('home'))

  if len(tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == select_content.idContent, tvSeasonContent.visibility == True)).all()) <= 0: return error(err_msg='Bu dizinin sezonları eklenmemiş.', ret_url=url_for('home'))

  select_first_season = tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == select_content.idContent)).order_by(tvSeasonContent.seasonNumber.asc()).first()
  if select_first_season == None: return error(err_msg='Uygun bir sezon bulunamadı.', ret_url=url_for('home'))

  return redirect(url_for('tv_season_title', title_url=title_url, season_number=select_first_season.seasonNumber))

@app.route('/tv/<title_url>/random-episode', methods=['POST', 'GET'])
@app.route('/dizi/<title_url>/rastgele-bolum', methods=['POST', 'GET'])
def tv_random_episode(title_url):
    if check_account() and not check_profile(): return redirect(url_for('whoiswatching'))

    select_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'TV')).first()
    if not select_content: return error(err_msg='Bu içerik bulunamadı.', ret_url=url_for('home'))

    select_all_players = tvPlayer.query.filter(tvPlayer.idContent == select_content.idContent).all()
    if not select_all_players: return error(err_msg='Bu dizi için uygun bir oynatıcı bulunamadı.', ret_url=url_for('tv_title', title_url=title_url))

    select_player = random.choice(select_all_players)

    return redirect(url_for('tv_watch', title_url=select_content.titleUrl, season_number=select_player.seasonNumber, episode_number=select_player.episodeNumber))

@app.route('/tv/<title_url>-season-<season_number>', methods=['POST', 'GET'])
@app.route('/dizi/<title_url>-sezon-<season_number>', methods=['POST', 'GET'])
def tv_season_title(title_url, season_number):
  if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

  select_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'TV')).first()
  if select_content == None: return error(err_msg='Bu içerik bulunamadı.', ret_url=url_for('home'))

  select_content.visitCount = select_content.visitCount + 1

  if len(tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == select_content.idContent, tvSeasonContent.visibility == True)).all()) <= 0: return error(err_msg='Bu dizinin sezonları eklenmemiş.', ret_url=url_for('home'))

  select_season = tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == select_content.idContent, tvSeasonContent.seasonNumber == season_number)).first()
  if select_season == None: return error(err_msg='Bu sezon bulunamadı.', ret_url=url_for('home'))

  select_season.visitCount = select_season.visitCount + 1
  db.session.commit()

  select_episodes = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == select_content.idContent, tvEpisodeContent.idTvSeason == select_season.idTvSeason)).order_by(tvEpisodeContent.episodeNumber.asc()).all()

  # CHECK ADULT BEGIN
  if select_content.adult == True:
    if check_profile() == True:
      if profile.query.filter(and_(profile.idAccount == session['ACCOUNT']['idAccount'], profile.idProfile == session['PROFILE']['idProfile'])).first().adult == False: return error(err_msg='Bu içerik çocuk hesabı için uygun değildir.', ret_url=url_for('home'))
      else: pass
    else: pass
  else: pass
  # CHECK ADULT END

  """
  # INTERSTITIAL BEGIN
  if check_admin() == True: pass
  else:
    get_interstitial = randint(0, 10)
    if get_interstitial == 1: return redirect(url_for('interstitial') + '?ret_url=' + url_for('tv_season_title', title_url=title_url, season_number=season_number))
  # INTERSTITIAL END
  """

  select_all_tags = contentTag.query.filter_by(idContent=select_content.idContent).order_by(contentTag.createDate.desc()).all()
  select_all_comments = tvTitleComment.query.filter(and_(tvTitleComment.idContent == select_content.idContent, tvTitleComment.idTvSeason == select_season.idTvSeason)).order_by(tvTitleComment.addDate.desc()).all()
  select_all_casts = contentCast.query.filter_by(idContent=select_content.idContent).order_by(contentCast.order.asc()).all()

  watchcommentform = WatchCommentForm()
  SELECTED_SPOILER = 0
  if request.form.getlist('contains_spoiler_box'): SELECTED_SPOILER = 1
  if watchcommentform.validate_on_submit():
    db.session.add(tvTitleComment(
      idContent = select_content.idContent,
      idTvSeason = select_season.idTvSeason,
      idAddProfile = session['PROFILE']['idProfile'],
      idAddAccount = session['ACCOUNT']['idAccount'],
      text = watchcommentform.text.data,
      replyTo = '',
      visibility = 1,
      spoiler = SELECTED_SPOILER,
      lastEditDate = datetime.now()
    ))
    db.session.commit()
    return redirect(url_for('tv_season_title', title_url=title_url, season_number=season_number))

  # KEYWORDS (TAGS) FOR SEO BEGIN
  get_tags = contentTag.query.filter(contentTag.idContent == select_content.idContent).all()
  get_tags_list = []
  for _ in get_tags: get_tags_list.append(_.title)
  get_tags_str = ', '.join(get_tags_list)
  # KEYWORDS (TAGS) FOR SEO END

  return render_template('tv/season/title.html', title=select_content.title + ' ' + str(select_season.seasonNumber) + '. Sezon', content_info=select_content, season_info=select_season, episodes_info=select_episodes, tags_info=select_all_tags, comments_info=select_all_comments, casts_info=select_all_casts, watchcommentform=watchcommentform, \
                                                  _META = {
                                                    'description': select_season.overview,
                                                    'keywords': get_tags_str,
                                                  })

@app.route('/tv/<title_url>-season-<season_number>/random-episode', methods=['POST', 'GET'])
@app.route('/dizi/<title_url>-sezon-<season_number>/rastgele-bolum', methods=['POST', 'GET'])
def tv_season_random_episode(title_url, season_number):
    if check_account() and not check_profile(): return redirect(url_for('whoiswatching'))

    select_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'TV')).first()
    if not select_content: return error(err_msg='Bu içerik bulunamadı.', ret_url=url_for('home'))

    select_season = tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == select_content.idContent, tvSeasonContent.seasonNumber == season_number)).first()
    if not select_content: return error(err_msg='Bu sezon bulunamadı.', ret_url=url_for('home'))

    select_all_players = tvPlayer.query.filter(tvPlayer.idContent == select_content.idContent, tvPlayer.idTvSeason == select_season.idTvSeason).all()
    if not select_all_players: return error(err_msg='Bu dizi için uygun bir oynatıcı bulunamadı.', ret_url=url_for('tv_title', title_url=title_url))

    select_player = random.choice(select_all_players)

    return redirect(url_for('tv_watch', title_url=select_content.titleUrl, season_number=select_player.seasonNumber, episode_number=select_player.episodeNumber))

@app.route('/tv/<title_url>-season-<season_number>-episode-<episode_number>', methods=['POST', 'GET'])
@app.route('/dizi/<title_url>-sezon-<season_number>-bolum-<episode_number>', methods=['POST', 'GET'])
def tv_watch(title_url, season_number, episode_number):
  if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

  select_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'TV')).first()
  if select_content == None: return error(err_msg='Bu içerik bulunamadı.', ret_url=url_for('home'))

  select_season = tvSeasonContent.query.filter(and_(tvSeasonContent.idContent == select_content.idContent, tvSeasonContent.seasonNumber == season_number)).first()
  if select_season == None: return error(err_msg='Bu sezon bulunamadı.', ret_url=url_for('home'))

  select_episode = tvEpisodeContent.query.filter(and_(tvEpisodeContent.idContent == select_content.idContent, tvEpisodeContent.idTvSeason == select_season.idTvSeason, tvEpisodeContent.episodeNumber == episode_number)).first()
  if select_episode == None: return error(err_msg='Bu bölüm bulunamadı.', ret_url=url_for('home'))

  select_episode.visitCount = select_episode.visitCount + 1
  db.session.commit()

  # SELECT PLAYER BEGIN
  if request.args.get('viewkey'):
    select_current_player = tvPlayer.query.filter(and_(tvPlayer.idContent == select_content.idContent, tvPlayer.viewKey == request.args.get('viewkey'), tvPlayer.seasonNumber == select_season.seasonNumber, tvPlayer.episodeNumber == select_episode.episodeNumber)).first()
    if select_current_player == None: return error(err_msg='Bu oynatıcı bulunamadı.', ret_url=url_for('home'))
  else:
    # IF THERE IS NO VIEWKEY ENTERED
    # THEN FIND THE FIRST ONE
    select_first_player = tvPlayer.query.filter(and_(tvPlayer.idContent == select_content.idContent, tvPlayer.seasonNumber == select_season.seasonNumber, tvPlayer.episodeNumber == select_episode.episodeNumber)).order_by(tvPlayer.order.asc()).first()
    if select_first_player == None: return error(err_msg='Bu oynatıcı bulunamadı.', ret_url=url_for('home'))
    return redirect(url_for('tv_watch', title_url=title_url, season_number=season_number, episode_number=episode_number) + '?viewkey=' + select_first_player.viewKey)
  # SELECT PLAYER END

  select_all_players = tvPlayer.query.filter(and_(tvPlayer.idContent == select_content.idContent, tvPlayer.idTvSeason == select_season.idTvSeason, tvPlayer.idTvEpisode == select_episode.idTvEpisode)).order_by(tvPlayer.order.asc()).all()

  # CHECK ADULT BEGIN
  if select_content.adult == True:
    if check_profile() == True:
      if profile.query.filter(and_(profile.idAccount == session['ACCOUNT']['idAccount'], profile.idProfile == session['PROFILE']['idProfile'])).first().adult == False: return error(err_msg='Bu içerik çocuk hesabı için uygun değildir.', ret_url=url_for('home'))
      else: pass
    else: pass
  else: pass
  # CHECK ADULT END

  # INTERSTITIAL BEGIN
  if check_admin() == True: pass
  else:
    get_interstitial = randint(0, 10)
    if get_interstitial == 1: return redirect(url_for('interstitial') + '?ret_url=' + url_for('tv_watch', title_url=title_url, season_number=season_number, episode_number=episode_number) + '?viewkey=' + select_current_player.viewKey)
  # INTERSTITIAL END

  select_all_tags = contentTag.query.filter_by(idContent=select_content.idContent).order_by(contentTag.createDate.desc()).all()
  select_all_comments = tvComment.query.filter(and_(tvComment.idContent == select_content.idContent, tvComment.idTvSeason == select_season.idTvSeason, tvComment.idTvEpisode == select_episode.idTvEpisode)).order_by(tvComment.addDate.desc()).all()
  select_all_casts = contentCast.query.filter_by(idContent=select_content.idContent).order_by(contentCast.order.asc()).all()
  select_recommendations = content.query.filter_by(type='TV').limit(12).all()

  watchcommentform = WatchCommentForm()
  SELECTED_SPOILER = 0
  if request.form.getlist('contains_spoiler_box'): SELECTED_SPOILER = 1
  if watchcommentform.validate_on_submit():
    db.session.add(tvComment(
      idContent = select_content.idContent,
      idTvSeason = select_season.idTvSeason,
      idTvEpisode = select_episode.idTvEpisode,
      idAddProfile = session['PROFILE']['idProfile'],
      idAddAccount = session['ACCOUNT']['idAccount'],
      text = watchcommentform.text.data,
      replyTo = '',
      visibility = 1,
      spoiler = SELECTED_SPOILER,
      lastEditDate = datetime.now()
    ))
    db.session.commit()
    return redirect(url_for('tv_watch', title_url=title_url, season_number=season_number, episode_number=episode_number) + '?viewkey=' + select_current_player.viewKey)

  # KEYWORDS (TAGS) FOR SEO BEGIN
  get_tags = contentTag.query.filter(contentTag.idContent == select_content.idContent).all()
  get_tags_list = []
  for _ in get_tags: get_tags_list.append(_.title)
  get_tags_str = ', '.join(get_tags_list)
  # KEYWORDS (TAGS) FOR SEO END

  return render_template('watch/index.html', title=select_content.title + ' ' + str(select_season.seasonNumber) + '. Sezon ' + str(select_episode.episodeNumber) + '. Bölüm', current_player_info=select_current_player, all_players_info=select_all_players, content_info=select_content, season_info=select_season, episode_info=select_episode, tags_info=select_all_tags, comments_info=select_all_comments, casts_info=select_all_casts, recommendations_info=select_recommendations, watchcommentform=watchcommentform, \
                                              _META = {
                                                'description': select_episode.overview,
                                                'keywords': get_tags_str,
                                              })
