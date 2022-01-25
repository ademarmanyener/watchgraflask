# -*- encoding: utf-8 -*-
from includes import *

@app.route('/adminpanel/comments')
@app.route('/yoneticipaneli/yorumlar')
def adminpanel_comments():
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_comments') + '?query=*&page=1&type=*&related_id=*&sort=newest&list_count=10'

  ARG_QUERY = request.args.get('query', default='*', type=str)
  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_TYPE = request.args.get('type', default='*', type=str)
  ARG_RELATED_ID = request.args.get('related_id', default='*', type=str)
  ARG_SORT = request.args.get('sort', default='newest', type=str)
  ARG_LIST_COUNT = request.args.get('list_count', default=10, type=int)
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL) 
  # page validation end

  # get query filters begin
  _db_table = movieComment
  if ARG_TYPE == 'movie':
    _db_table = movieComment
  if ARG_TYPE == 'tv':
    _db_table = tvComment
  if ARG_TYPE == 'tv_title':
    _db_table = tvTitleComment
  if ARG_TYPE == 'cast':
    _db_table = castComment

  if not ARG_RELATED_ID == '*':
    if ARG_TYPE == 'movie':
      _db_related_id_content_id = _db_table.idContent.like('%{}%'.format(ARG_RELATED_ID))
      _db_related_id_add_profile_id = _db_table.idAddProfile.like('%{}%'.format(ARG_RELATED_ID))
      _db_related_id_add_account_id = _db_table.idAddAccount.like('%{}%'.format(ARG_RELATED_ID))
    if ARG_TYPE == 'tv':
      _db_related_id_content_id = _db_table.idContent.like('%{}%'.format(ARG_RELATED_ID))
      _db_related_id_season_id = _db_table.idContent.like('%{}%'.format(ARG_RELATED_ID))
      _db_related_id_episode_id = _db_table.idContent.like('%{}%'.format(ARG_RELATED_ID))
      _db_related_id_add_profile_id = _db_table.idAddProfile.like('%{}%'.format(ARG_RELATED_ID))
      _db_related_id_add_account_id = _db_table.idAddAccount.like('%{}%'.format(ARG_RELATED_ID))
    if ARG_TYPE == 'tv_title':
      _db_related_id_content_id = _db_table.idContent.like('%{}%'.format(ARG_RELATED_ID))
      _db_related_id_season_id = _db_table.idContent.like('%{}%'.format(ARG_RELATED_ID))
      _db_related_id_add_profile_id = _db_table.idAddProfile.like('%{}%'.format(ARG_RELATED_ID))
      _db_related_id_add_account_id = _db_table.idAddAccount.like('%{}%'.format(ARG_RELATED_ID))
    if ARG_TYPE == 'cast':
      _db_related_id_cast_id = _db_table.idCast.like('%{}%'.format(ARG_RELATED_ID))
      _db_related_id_add_profile_id = _db_table.idAddProfile.like('%{}%'.format(ARG_RELATED_ID))
      _db_related_id_add_account_id = _db_table.idAddAccount.like('%{}%'.format(ARG_RELATED_ID))

  if not ARG_QUERY == '*':
    _db_query_id = _db_table.idComment.like('%{}%'.format(ARG_QUERY))
    _db_query_text = _db_table.text.like('%{}%'.format(ARG_QUERY))
  else:
    _db_query_id = _db_table.idComment.like('%%')
    _db_query_text = _db_table.text.like('%%')

  if ARG_SORT == 'a-to-z': _db_sort = _db_table.text.asc() 
  if ARG_SORT == 'z-to-a': _db_sort = _db_table.text.desc() 
  if ARG_SORT == 'newest': _db_sort = _db_table.addDate.desc()
  if ARG_SORT == 'oldest': _db_sort = _db_table.addDate.asc()
  # get query filters end

  get_comments = _db_table.query.filter(or_(_db_query_id, _db_query_text)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(_db_table.query.filter(or_(_db_query_id, _db_query_text)).all()) / ARG_LIST_COUNT)
  if not ARG_RELATED_ID == '*':
    if ARG_TYPE == 'movie':
      get_comments = _db_table.query.filter(or_(_db_related_id_content_id, _db_related_id_add_profile_id, _db_related_id_add_account_id)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
      DEF_PAGE_MAX = ceil(len(_db_table.query.filter(or_(_db_related_id_content_id, _db_related_id_add_profile_id, _db_related_id_add_account_id)).all()) / ARG_LIST_COUNT)
    if ARG_TYPE == 'tv':
      get_comments = _db_table.query.filter(or_(_db_related_id_content_id, _db_related_id_season_id, _db_related_id_episode_id, _db_related_id_add_profile_id, _db_related_id_add_account_id)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
      DEF_PAGE_MAX = ceil(len(_db_table.query.filter(or_(_db_related_id_content_id, _db_related_id_season_id, _db_related_id_episode_id, _db_related_id_add_profile_id, _db_related_id_add_account_id)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()) / ARG_LIST_COUNT)
    if ARG_TYPE == 'tv_title':
      get_comments = _db_table.query.filter(or_(_db_related_id_content_id, _db_related_id_season_id, _db_related_id_add_profile_id, _db_related_id_add_account_id)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
      DEF_PAGE_MAX = ceil(len(_db_table.query.filter(or_(_db_related_id_content_id, _db_related_id_season_id, _db_related_id_add_profile_id, _db_related_id_add_account_id)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()) / ARG_LIST_COUNT)
    if ARG_TYPE == 'cast':
      get_comments = _db_table.query.filter(or_(_db_related_id_cast_id, _db_related_id_add_profile_id, _db_related_id_add_account_id)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
      DEF_PAGE_MAX = ceil(len(_db_table.query.filter(or_(_db_related_id_cast_id, _db_related_id_add_profile_id, _db_related_id_add_account_id)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()) / ARG_LIST_COUNT)

  # url args validation begin
  if not request.args.get('query') or not request.args.get('page') or not request.args.get('type') or not request.args.get('related_id') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
  # url args validation end 

  return render_template('adminpanel/comments/list.html', title='Tüm Yorumlar', comments_info=get_comments, \
                                        _ARG = {
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'type': ARG_TYPE,
                                          'related_id': ARG_RELATED_ID,
                                          'sort': ARG_SORT,
                                          'list_count': ARG_LIST_COUNT,
                                        })

# ! FIX THIS PAGE

@app.route('/adminpanel/comment/edit', methods=['POST', 'GET'])
@app.route('/yoneticipaneli/yorum/duzenle', methods=['POST', 'GET'])
def adminpanel_comment_edit():
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_home')

  ARG_COMMENT_ID = request.args.get('c_id', default='*', type=str)
  ARG_COMMENT_TYPE = request.args.get('c_type', default='*', type=str)

  # url args validation begin
  if not request.args.get('c_id') or not request.args.get('c_type'): return redirect(RET_URL)
  # url args validation end 

  if ARG_COMMENT_TYPE == 'movie':
    get_comment = movieComment.query.filter_by(idComment=ARG_COMMENT_ID).first()
  elif ARG_COMMENT_TYPE == 'tv':
    get_comment = tvComment.query.filter_by(idComment=ARG_COMMENT_ID).first()
  elif ARG_COMMENT_TYPE == 'tv_title':
    get_comment = tvTitleComment.query.filter_by(idComment=ARG_COMMENT_ID).first()
  elif ARG_COMMENT_TYPE == 'cast':
    get_comment = castComment.query.filter_by(idComment=ARG_COMMENT_ID).first()
  else: return redirect(RET_URL) 

  if not get_comment: return redirect(RET_URL)

  # form begin
  if request.method == 'POST':
    DEF_NEW_TEXT = request.form['input___text']
    DEF_NEW_REPLY_TO = request.form['input___replyTo']

    DEF_NEW_VISIBILITY = int(request.form['select2___visibility'])
    if not ARG_COMMENT_TYPE == 'cast': DEF_NEW_SPOILER = int(request.form['select2___spoiler'])

    get_comment.text = DEF_NEW_TEXT
    get_comment.replyTo = DEF_NEW_REPLY_TO
    get_comment.visibility = DEF_NEW_VISIBILITY
    if not ARG_COMMENT_TYPE == 'cast': get_comment.spoiler = DEF_NEW_SPOILER

    db.session.commit()

    return redirect(url_for('adminpanel_comment_edit') + '?c_id={}&c_type={}'.format(ARG_COMMENT_ID, ARG_COMMENT_TYPE))
  # form end
  
  return render_template('adminpanel/comments/edit.html', title='Düzenleniyor: {}'.format(get_comment.text), comment_info=get_comment, \
                                        _ARG = {
                                          'c_id': ARG_COMMENT_ID,
                                          'c_type': ARG_COMMENT_TYPE,
                                        })
