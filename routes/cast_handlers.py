# -*- encoding: utf-8 -*-
from includes import *

@app.route('/cast/title/func/<function>/proc', methods=['POST'])
def cast_title_func_proc(function):
  if request.is_json == False: return error(err_msg='JSON değil.')

  if function == 'send_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_cast_id = request.get_json()['idCast']
    get_text = request.get_json()['text']

    if get_text:
      db.session.add(castComment(
        idCast = get_cast_id,
        idAddProfile = session['PROFILE']['idProfile'],
        idAddAccount = session['ACCOUNT']['idAccount'],
        text = get_text,
        replyTo = '',
        visibility = 1,
        lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
      ))
      db.session.commit()

      latest_comment =  castComment.query.filter(and_(castComment.idCast == get_cast_id, castComment.replyTo == '', castComment.idAddProfile == session['PROFILE']['idProfile'], castComment.idAddAccount == session['ACCOUNT']['idAccount'])).order_by(castComment.addDate.desc()).first()
      if latest_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

      return make_response(jsonify({'succ_msg': 'Yorumunuz başarıyla gönderildi!', \
                                    'latest_comment_id': latest_comment.idComment, \
                                    'latest_comment_text': latest_comment.text, \
                                    }))
    else: return make_response(jsonify({'err_msg': 'Boş yorum yapılamaz.'}))

  if function == 'send_reply':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_cast_id = request.get_json()['idCast']
    get_reply = request.get_json()['reply']
    get_reply_to = request.get_json()['replyTo']

    if get_reply and get_reply_to:
      if castComment.query.filter_by(idComment=get_reply_to).first() == None: return make_response(jsonify({'err_msg': 'Olmayan bir yoruma mı yanıt göndericeksin?'}))

      db.session.add(castComment(
        idCast = get_cast_id,
        idAddProfile = session['PROFILE']['idProfile'],
        idAddAccount = session['ACCOUNT']['idAccount'],
        text = get_reply,
        replyTo = get_reply_to,
        visibility = 1,
        lastEditDate = datetime.now(pytz.timezone(PY_TIMEZONE)),
      ))
      db.session.commit()

      latest_reply =  castComment.query.filter(and_(castComment.idCast == get_cast_id, castComment.replyTo != '', castComment.idAddProfile == session['PROFILE']['idProfile'], castComment.idAddAccount == session['ACCOUNT']['idAccount'])).order_by(castComment.addDate.desc()).first()
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

    get_cast_id = request.get_json()['idCast']
    get_comment_id = request.get_json()['idComment']

    get_comment = castComment.query.filter(and_(castComment.idCast == get_cast_id, castComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    return make_response(jsonify({'succ_msg': 'YES', \
                                  'selected_comment_text': get_comment.text, \
                                  }))

  if function == 'delete_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_cast_id = request.get_json()['idCast']
    get_comment_id = request.get_json()['idComment']

    get_comment = castComment.query.filter(and_(castComment.idCast == get_cast_id, castComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))
    if get_comment.idAddProfile == session['PROFILE']['idProfile'] and get_comment.idAddAccount == session['ACCOUNT']['idAccount']: pass
    else: return make_response(jsonify({'err_msg': 'Bu yorumun sizin profilinize ait olduğuna emin misiniz?'}))

    get_comment.drop()

    return make_response(jsonify({'succ_msg': 'Yorumunuz başarıyla silindi!', 'deleted_comment_id': get_comment.idComment}))

  if function == 'like_comment':
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_cast_id = request.get_json()['idCast']
    get_comment_id = request.get_json()['idComment']

    get_comment = castComment.query.filter(and_(castComment.idCast == get_cast_id, castComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    get_comment_rate = castCommentRate.query.filter(and_(castCommentRate.idCast == get_cast_id, castCommentRate.idComment == get_comment_id, castCommentRate.idRateProfile == session['PROFILE']['idProfile'], castCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], castCommentRate.rateType == 'LIKE')).first()
    if get_comment_rate == None:
      if get_comment.idAddAccount == session['ACCOUNT']['idAccount'] and get_comment.idAddProfile == session['PROFILE']['idProfile']:
        return make_response(jsonify({'err_msg': 'Kendi profiliniz tarafından yapılan yorumları beğenemezsiniz.'}))
      else:
        db.session.add(castCommentRate(
          idCast = get_cast_id,
          idComment = get_comment_id,
          idRateProfile = session['PROFILE']['idProfile'],
          idRateAccount = session['ACCOUNT']['idAccount'],
          rateType = 'LIKE',
        ))
        db.session.commit()

        # if the profile has disliked the comment, then drop it first
        select_dislike = castCommentRate.query.filter(and_(castCommentRate.idCast == get_cast_id, castCommentRate.idComment == get_comment_id, castCommentRate.idRateProfile == session['PROFILE']['idProfile'], castCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], castCommentRate.rateType == 'DISLIKE')).first()
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

    get_cast_id = request.get_json()['idCast']
    get_comment_id = request.get_json()['idComment']

    get_comment = castComment.query.filter(and_(castComment.idCast == get_cast_id, castComment.idComment == get_comment_id)).first()
    if get_comment == None: return make_response(jsonify({'err_msg': 'Böyle bir yorum bulunamadı.'}))

    get_comment_rate = castCommentRate.query.filter(and_(castCommentRate.idCast == get_cast_id, castCommentRate.idComment == get_comment_id, castCommentRate.idRateProfile == session['PROFILE']['idProfile'], castCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], castCommentRate.rateType == 'DISLIKE')).first()
    if get_comment_rate == None:
      if get_comment.idAddAccount == session['ACCOUNT']['idAccount'] and get_comment.idAddProfile == session['PROFILE']['idProfile']:
        return make_response(jsonify({'err_msg': 'Kendi profiliniz tarafından yapılan yorumlara dislike atamazsın.'}))
      else:
        db.session.add(castCommentRate(
          idCast = get_cast_id,
          idComment = get_comment_id,
          idRateProfile = session['PROFILE']['idProfile'],
          idRateAccount = session['ACCOUNT']['idAccount'],
          rateType = 'DISLIKE',
        ))
        db.session.commit()

        # if the profile has liked the comment, then drop it first
        select_like = castCommentRate.query.filter(and_(castCommentRate.idCast == get_cast_id, castCommentRate.idComment == get_comment_id, castCommentRate.idRateProfile == session['PROFILE']['idProfile'], castCommentRate.idRateAccount == session['ACCOUNT']['idAccount'], castCommentRate.rateType == 'LIKE')).first()
        if select_like:
          select_like.drop()
          return make_response(jsonify({'gave_dislike': 'Başarıyla dislikledınız!', 'took_like': 'OK'}))

        return make_response(jsonify({'gave_dislike': 'Başarıyla dislikledınız!'}))
    else:
      get_comment_rate.drop()
      return make_response(jsonify({'took_dislike': 'Dislikeyi geri aldınız.'}))

@app.route('/cast')
@app.route('/oyuncular')
def cast_discover():
  if check_account() and not check_profile(): return redirect(url_for('whoiswatching'))

  RET_URL = url_for('cast_discover') + '?query=*&page=1&gender=*'

  ARG_QUERY = request.args.get('query', default='*', type=str)
  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_GENDER = request.args.get('gender', default='*', type=str)
  ARG_LIST_COUNT = 48
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL)
  # page validation end

  # get query filters begin
  if not ARG_QUERY == "*": _db_query = cast.name.like('%{}%'.format(ARG_QUERY))
  else: _db_query = cast.name.like('%%')

  if not ARG_GENDER == "*":
    if ARG_GENDER == 'female': _db_gender = cast.gender == 1
    elif ARG_GENDER == 'male': _db_gender = cast.gender == 2
    else: _db_gender = cast.gender.like('%%')
  else: _db_gender = cast.gender.like('%%')
  # get query filters end

  get_results = cast.query.filter(and_(_db_query, _db_gender)).order_by(cast.name.asc()).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()

  return render_template('cast/discover.html', title='İçerikler', list_results_info=get_results, \
                                        _ARG = {
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': ceil(len(cast.query.filter(and_(_db_query, _db_gender)).all()) / ARG_LIST_COUNT),
                                          'gender': ARG_GENDER,
                                          'list_count': ARG_LIST_COUNT,
                                        })

@app.route('/cast/<name_url>', methods=['POST', 'GET'])
@app.route('/oyuncu/<name_url>', methods=['POST', 'GET'])
def cast_title(name_url):
  if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

  select_cast = cast.query.filter_by(nameUrl=name_url).first()
  if not select_cast: return error(err_msg='Böyle bir oyuncu bulunamadı.')

  select_cast_contents = contentCast.query.filter_by(idCast=select_cast.idCast).all()
  select_all_comments = castComment.query.filter_by(idCast=select_cast.idCast).order_by(castComment.addDate.desc()).all()

  return render_template('cast/title.html', title=select_cast.name, cast_info=select_cast, cast_contents_info=select_cast_contents, comments_info=select_all_comments)
