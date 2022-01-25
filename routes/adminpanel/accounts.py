# -*- encoding: utf-8 -*-
from includes import *

@app.route('/adminpanel/accounts')
@app.route('/yoneticipaneli/hesaplar')
def adminpanel_accounts():
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_accounts') + '?query=*&page=1&sort=newest&list_count=10'

  ARG_QUERY = request.args.get('query', default='*', type=str)
  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_SORT = request.args.get('sort', default='newest', type=str)
  ARG_LIST_COUNT = request.args.get('list_count', default=10, type=int)
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL) 
  # page validation end

  # get query filters begin
  if not ARG_QUERY == '*':
    _db_query_id = account.idAccount.like('%{}%'.format(ARG_QUERY))
    _db_query_username = account.username.like('%{}%'.format(ARG_QUERY))
  else:
    _db_query_id = account.idAccount.like('%%')
    _db_query_username = account.username.like('%%')

  if ARG_SORT == 'a-to-z': _db_sort = account.username.asc() 
  if ARG_SORT == 'z-to-a': _db_sort = account.username.desc() 
  if ARG_SORT == 'newest': _db_sort = account.signupDate.desc()
  if ARG_SORT == 'oldest': _db_sort = account.signupDate.asc()

  get_results = account.query.filter(or_(_db_query_id, _db_query_username)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(account.query.filter(or_(_db_query_id, _db_query_username)).all()) / ARG_LIST_COUNT)
  # get query filters end

  # url args validation begin
  if not request.args.get('query') or not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
  # url args validation end 

  return render_template('adminpanel/accounts/list.html', title='Tüm Hesaplar', list_results_info=get_results, \
                                        _ARG = {
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'sort': ARG_SORT,
                                          'list_count': ARG_LIST_COUNT,
                                        })

@app.route('/adminpanel/account/<username>/edit', methods=['POST', 'GET'])
@app.route('/yoneticipaneli/hesap/<username>/duzenle', methods=['POST', 'GET'])
def adminpanel_account_edit(username):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_home')

  get_account = account.query.filter(account.username == username).first()
  if not get_account: return redirect(RET_URL)

  # form begin
  if request.method == 'POST':
    DEF_NEW_USERNAME = request.form['input___username']
    DEF_NEW_EMAIL_ADDRESS = request.form['input___emailAddress']
    DEF_NEW_PASSWORD = request.form['input___password']
    DEF_NEW_SECURITY_PASSWORD = request.form['input___securityPassword']
    DEF_NEW_PERMISSION = request.form['select2___permission']

    # variable validation begin
    if not DEF_NEW_USERNAME: return error(err_msg='Kullanıcı adını boş bıraktınız.', ret_url=RET_URL)
    # variable validation end

    check_account = account.query.filter(and_(account.idAccount != get_account.idAccount, account.username == DEF_NEW_USERNAME)).first()
    if check_account: return error(err_msg='Bu kullanıcı adı zaten kullanımda.', ret_url=RET_URL)

    get_account.username = DEF_NEW_USERNAME
    get_account.emailAddress = DEF_NEW_EMAIL_ADDRESS
    # password
    if DEF_NEW_PASSWORD: 
      get_account.password = hash_str_hash(get_str=DEF_NEW_PASSWORD)

    if DEF_NEW_SECURITY_PASSWORD:
      get_account.securityPassword = hash_str_hash(get_str=DEF_NEW_SECURITY_PASSWORD)
    # end password
    get_account.permission = DEF_NEW_PERMISSION

    db.session.commit()

    return redirect(url_for('adminpanel_account_edit', username=DEF_NEW_USERNAME))
    return redirect(url_for('adminpanel_content_edit', title_url=DEF_NEW_TITLE_URL))
  # form end 

  return render_template('adminpanel/accounts/edit.html', title='Düzenleniyor: {}'.format(get_account.username), account_info=get_account)
