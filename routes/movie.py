# -*- encoding: utf-8 -*-
from includes import *

@app.route('/movie/watch/func/<function>/proc', methods=['POST'])
def movie_watch_func_proc(function):
  if request.is_json == False: return error(err_msg='JSON değil.')

  if function == 'send_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_text = request.get_json()['text']
    get_contains_spoiler = request.get_json()['contains_spoiler']

    SELECTED_SPOILER = 0
    if get_contains_spoiler: SELECTED_SPOILER = 1

    if get_text:
      db.session.add(movieComment(
        idContent = get_content_id,
        idAddProfile = get_logged_profile().idProfile,
        idAddAccount = get_logged_account().idAccount,
        text = get_text,
        replyTo = '',
        visibility = 1,
        spoiler = SELECTED_SPOILER,
        lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
      ))
      db.session.commit()

      latest_comment =  movieComment.query.filter(and_(movieComment.idContent == get_content_id, movieComment.replyTo == '', movieComment.idAddProfile == get_logged_profile().idProfile, movieComment.idAddAccount == get_logged_account().idAccount)).order_by(movieComment.addDate.desc()).first()
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
    get_reply = request.get_json()['reply']
    get_reply_to = request.get_json()['replyTo']

    if get_reply and get_reply_to:
      if movieComment.query.filter_by(idComment=get_reply_to).first() == None: return make_response(jsonify({'err_msg': 'Olmayan bir yoruma mı yanıt göndericeksin?'}))

      db.session.add(movieComment(
        idContent = get_content_id,
        idAddProfile = get_logged_profile().idProfile,
        idAddAccount = get_logged_account().idAccount,
        text = get_reply,
        replyTo = get_reply_to,
        visibility = 1,
        spoiler = 0,
        lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
      ))
      db.session.commit()

      latest_reply =  movieComment.query.filter(and_(movieComment.idContent == get_content_id, movieComment.replyTo != '', movieComment.idAddProfile == get_logged_profile().idProfile, movieComment.idAddAccount == get_logged_account().idAccount)).order_by(movieComment.addDate.desc()).first()
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
    get_comment_id = request.get_json()['idComment']

    get_comment = movieComment.query.filter(and_(movieComment.idContent == get_content_id, movieComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    return make_response(jsonify({'succ_msg': 'YES', \
                                  'selected_comment_text': get_comment.text, \
                                  }))

  if function == 'delete_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_comment_id = request.get_json()['idComment']

    get_comment = movieComment.query.filter(and_(movieComment.idContent == get_content_id, movieComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))
    if get_comment.idAddProfile == get_logged_profile().idProfile and get_comment.idAddAccount == get_logged_account().idAccount: pass
    else: return make_response(jsonify({'err_msg': 'Bu yorumun sizin profilinize ait olduğuna emin misiniz?'}))

    get_comment.drop()

    return make_response(jsonify({'succ_msg': 'Yorumunuz başarıyla silindi!', 'deleted_comment_id': get_comment.idComment}))

  if function == 'like_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_content_id = request.get_json()['idContent']
    get_comment_id = request.get_json()['idComment']

    get_comment = movieComment.query.filter(and_(movieComment.idContent == get_content_id, movieComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    get_comment_rate = movieCommentRate.query.filter(and_(movieCommentRate.idContent == get_content_id, movieCommentRate.idComment == get_comment_id, movieCommentRate.idRateProfile == get_logged_profile().idProfile, movieCommentRate.idRateAccount == get_logged_account().idAccount, movieCommentRate.rateType == 'LIKE')).first()
    if get_comment_rate == None:
      if get_comment.idAddAccount == get_logged_account().idAccount and get_comment.idAddProfile == get_logged_profile().idProfile:
        return make_response(jsonify({'err_msg': 'Kendi profiliniz tarafından yapılan yorumları beğenemezsiniz.'}))
      else:
        db.session.add(movieCommentRate(
          idContent = get_content_id,
          idComment = get_comment_id,
          idRateProfile = get_logged_profile().idProfile,
          idRateAccount = get_logged_account().idAccount,
          rateType = 'LIKE',
        ))
        db.session.commit()

        # if the profile has disliked the comment, then drop it first
        select_dislike = movieCommentRate.query.filter(and_(movieCommentRate.idContent == get_content_id, movieCommentRate.idComment == get_comment_id, movieCommentRate.idRateProfile == get_logged_profile().idProfile, movieCommentRate.idRateAccount == get_logged_account().idAccount, movieCommentRate.rateType == 'DISLIKE')).first()
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
    get_comment_id = request.get_json()['idComment']

    get_comment = movieComment.query.filter(and_(movieComment.idContent == get_content_id, movieComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    get_comment_rate = movieCommentRate.query.filter(and_(movieCommentRate.idContent == get_content_id, movieCommentRate.idComment == get_comment_id, movieCommentRate.idRateProfile == get_logged_profile().idProfile, movieCommentRate.idRateAccount == get_logged_account().idAccount, movieCommentRate.rateType == 'DISLIKE')).first()
    if get_comment_rate == None:
      if get_comment.idAddAccount == get_logged_account().idAccount and get_comment.idAddProfile == get_logged_profile().idProfile:
        return make_response(jsonify({'err_msg': 'Kendi profiliniz tarafından yapılan yorumlara dislike atamazsın.'}))
      else:
        db.session.add(movieCommentRate(
          idContent = get_content_id,
          idComment = get_comment_id,
          idRateProfile = get_logged_profile().idProfile,
          idRateAccount = get_logged_account().idAccount,
          rateType = 'DISLIKE',
        ))
        db.session.commit()

        # if the profile has liked the comment, then drop it first
        select_like = movieCommentRate.query.filter(and_(movieCommentRate.idContent == get_content_id, movieCommentRate.idComment == get_comment_id, movieCommentRate.idRateProfile == get_logged_profile().idProfile, movieCommentRate.idRateAccount == get_logged_account().idAccount, movieCommentRate.rateType == 'LIKE')).first()
        if select_like:
          select_like.drop()
          return make_response(jsonify({'gave_dislike': 'Başarıyla dislikledınız!', 'took_like': 'OK'}))

        return make_response(jsonify({'gave_dislike': 'Başarıyla dislikledınız!'}))
    else:
      get_comment_rate.drop()
      return make_response(jsonify({'took_dislike': 'Dislikeyi geri aldınız.'}))

@app.route('/movie/<title_url>', methods=['POST', 'GET'])
@app.route('/film/<title_url>', methods=['POST', 'GET'])
def movie_watch(title_url):
  if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

  select_content = content.query.filter(and_(content.titleUrl == title_url, content.type == 'MOVIE')).first()
  if select_content == None: return error(err_msg='Bu içerik bulunamadı.', ret_url=url_for('home'))

  select_content.visitCount = select_content.visitCount + 1
  db.session.commit()

  # SELECT PLAYER BEGIN
  if request.args.get('viewkey'):
    select_current_player = moviePlayer.query.filter(and_(moviePlayer.idContent == select_content.idContent, moviePlayer.viewKey == request.args.get('viewkey'))).first()
    if select_current_player == None: return error(err_msg='Bu oynatıcı bulunamadı.', ret_url=url_for('home'))
  else:
    # IF THERE IS NO VIEWKEY ENTERED
    # THEN FIND THE FIRST ONE
    select_first_player = moviePlayer.query.filter(and_(moviePlayer.idContent == select_content.idContent)).order_by(moviePlayer.order.asc()).first()
    if select_first_player == None: return error(err_msg='Bu oynatıcı bulunamadı.', ret_url=url_for('home'))
    return redirect(url_for('movie_watch', title_url=title_url) + '?viewkey=' + select_first_player.viewKey)
  # SELECT PLAYER END

  select_all_players = moviePlayer.query.filter(and_(moviePlayer.idContent == select_content.idContent)).order_by(moviePlayer.order.asc()).all()

  # CHECK ADULT BEGIN
  if select_content.adult == True:
      if check_profile() == True:
          if profile.query.filter(and_(profile.idAccount == get_logged_account().idAccount, profile.idProfile == get_logged_profile().idProfile)).first().adult == False: return error(err_msg='Bu içerik çocuk hesabı için uygun değildir.', ret_url=url_for('home'))
          else: pass
      else: pass
  else: pass
  # CHECK ADULT END


  """
  # INTERSTITIAL BEGIN
  if check_admin() == True: pass
  else:
      get_interstitial = randint(0, 10)
      if get_interstitial == 1: return redirect(url_for('interstitial') + '?ret_url=' + url_for('movie_watch', title_url=select_content.titleUrl) + '?viewkey=' + select_current_player.viewKey)
  # INTERSTITIAL END
  """

  select_all_tags = contentTag.query.filter_by(idContent=select_content.idContent).order_by(contentTag.createDate.desc()).all()
  select_all_comments = movieComment.query.filter_by(idContent=select_content.idContent).order_by(movieComment.addDate.desc()).all()
  select_all_casts = contentCast.query.filter_by(idContent=select_content.idContent).order_by(contentCast.order.asc()).all()
  select_recommendations = content.query.filter_by(type='MOVIE').limit(12).all()

  watchcommentform = WatchCommentForm()
  SELECTED_SPOILER = 0
  if request.form.getlist('contains_spoiler_box'): SELECTED_SPOILER = 1
  if watchcommentform.validate_on_submit():
    db.session.add(movieComment(
      idContent = select_content.idContent,
      idAddProfile = get_logged_profile().idProfile,
      idAddAccount = get_logged_account().idAccount,
      text = watchcommentform.text.data,
      replyTo = '',
      visibility = 1,
      spoiler = SELECTED_SPOILER,
      lastEditDate = datetime.now()
    ))
    db.session.commit()
    return redirect(url_for('movie_watch', title_url=select_content.titleUrl) + '?viewkey=' + select_current_player.viewKey)

  # KEYWORDS (TAGS) FOR SEO BEGIN
  get_tags = contentTag.query.filter(contentTag.idContent == select_content.idContent).all()
  get_tags_list = []
  for _ in get_tags: get_tags_list.append(_.title)
  get_tags_str = ', '.join(get_tags_list)
  # KEYWORDS (TAGS) FOR SEO END

  return render_template('watch/index.html', title=select_content.title, current_player_info=select_current_player, all_players_info=select_all_players, content_info=select_content, tags_info=select_all_tags, comments_info=select_all_comments, casts_info=select_all_casts, recommendations_info=select_recommendations, watchcommentform=watchcommentform, \
                                              _META = {
                                                'description': select_content.overview,
                                                'keywords': get_tags_str,
                                              })
