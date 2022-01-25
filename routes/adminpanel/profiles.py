# -*- encoding: utf-8 -*-
from includes import *

@app.route('/adminpanel/profiles')
@app.route('/yoneticipaneli/profiller')
def adminpanel_profiles():
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_profiles') + '?query=*&page=1&account=*&sort=newest&list_count=10'

  ARG_QUERY = request.args.get('query', default='*', type=str)
  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_ACCOUNT = request.args.get('account', default='*', type=str)
  ARG_SORT = request.args.get('sort', default='newest', type=str)
  ARG_LIST_COUNT = request.args.get('list_count', default=10, type=int)
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL) 
  # page validation end

  # get query filters begin
  if not ARG_QUERY == '*':
    _db_query_id = profile.idProfile.like('%{}%'.format(ARG_QUERY))
    _db_query_username = profile.username.like('%{}%'.format(ARG_QUERY))
  else:
    _db_query_id = profile.idProfile.like('%%')
    _db_query_username = profile.username.like('%%')

  if ARG_SORT == 'a-to-z': _db_sort = profile.username.asc() 
  if ARG_SORT == 'z-to-a': _db_sort = profile.username.desc() 
  if ARG_SORT == 'newest': _db_sort = profile.addDate.desc()
  if ARG_SORT == 'oldest': _db_sort = profile.addDate.asc()

  if not ARG_ACCOUNT == '*':
    get_account = account.query.filter(account.username == ARG_ACCOUNT).first()
    if not get_account: return redirect(RET_URL)

    get_profiles = profile.query.filter(and_(or_(_db_query_id, _db_query_username), profile.idAccount == get_account.idAccount)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
    DEF_PAGE_MAX = ceil(len(profile.query.filter(and_(or_(_db_query_id, _db_query_username), profile.idAccount == get_account.idAccount)).all()) / ARG_LIST_COUNT)
  else:
    get_profiles = profile.query.filter(or_(_db_query_id, _db_query_username)).order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
    DEF_PAGE_MAX = ceil(len(profile.query.filter(or_(_db_query_id, _db_query_username)).all()) / ARG_LIST_COUNT)
  # get query filters end

  # url args validation begin
  if not request.args.get('page') or not request.args.get('account') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
  # url args validation end 

  return render_template('adminpanel/profiles/list.html', title='Tüm Profiller', profiles_info=get_profiles, \
                                        _ARG = {
                                          'query': ARG_QUERY,
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'account': ARG_ACCOUNT,
                                          'sort': ARG_SORT,
                                          'list_count': ARG_LIST_COUNT,
                                        })

@app.route('/adminpanel/profiles/account/<account_username>/profile/<profile_username>/edit', methods=['POST', 'GET'])
@app.route('/yoneticipaneli/profiller/hesap/<account_username>/profile/<profile_username>/duzenle', methods=['POST', 'GET'])
def adminpanel_profile_edit(account_username, profile_username):
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_home')

  get_account = account.query.filter(account.username == account_username).first()
  if not get_account: return redirect(RET_URL)

  get_profile = profile.query.filter(and_(profile.idAccount == get_account.idAccount, profile.username == profile_username)).first()
  if not get_profile: return redirect(RET_URL)

  try:
    get_avatars_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'account', get_account.idAccount, 'profile', get_profile.idProfile, 'avatar'))
    get_backgrounds_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'account', get_account.idAccount, 'profile', get_profile.idProfile, 'background'))
  except:
    get_avatars_list = ''
    get_backgrounds_list = ''

  # form begin
  if request.method == 'POST':
    DEF_NEW_USERNAME = request.form['input___username']
    DEF_NEW_PASSWORD = request.form['input___password']
    DEF_NEW_BIOGRAPHY = request.form['input___biography']
    # IMAGE UPLOAD BEGIN
    DEF_NEW_IMAGE_AVATAR = get_profile.imageAvatar
    DEF_NEW_IMAGE_BACKGROUND = get_profile.imageBackground
    try:
      if request.form.getlist('avatar'):
        DEF_NEW_IMAGE_AVATAR = '/storage/account/{}/profile/{}/avatar/{}'.format(get_account.idAccount, get_profile.idProfile, request.form.getlist('avatar')[0])
      else:
        temp_new_uploaded_avatar = request.files['form__img-upload']
        if temp_new_uploaded_avatar:
          temp_secure_filename = secure_filename(temp_new_uploaded_avatar.filename)
          temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
          temp_new_uploaded_avatar.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'account', get_account.idAccount, 'profile', get_profile.idProfile, 'avatar', temp_generate_filename))
          DEF_NEW_IMAGE_AVATAR = '/storage/account/{}/profile/{}/avatar/{}'.format(get_account.idAccount, get_profile.idProfile, temp_generate_filename)
        else:
          DEF_NEW_IMAGE_AVATAR = request.form['input___imageAvatar']

      if request.form.getlist('background'):
        DEF_NEW_IMAGE_BACKGROUND = '/storage/account/{}/profile/{}/background/{}'.format(get_account.idAccount, get_profile.idProfile, request.form.getlist('background')[0])
      else:
        temp_new_uploaded_background = request.files['form__imgBg-upload']
        if temp_new_uploaded_background:
          temp_secure_filename = secure_filename(temp_new_uploaded_background.filename)
          temp_generate_filename = str(id_generator(chars=string.digits, size=16)) + '.' + str(temp_secure_filename.split('.')[1])
          temp_new_uploaded_background.save(os.path.join(os.path.dirname(app.instance_path), 'storage', 'account', get_account.idAccount, 'profile', get_profile.idProfile, 'background', temp_generate_filename))
          DEF_NEW_IMAGE_BACKGROUND = '/storage/account/{}/profile/{}/background/{}'.format(get_account.idAccount, get_profile.idProfile, temp_generate_filename)
        else:
          DEF_NEW_IMAGE_BACKGROUND = request.form['input___imageBackground']
    except: pass
    # IMAGE UPLOAD END 
    DEF_NEW_ADULT = request.form['select2___adult']
    DEF_NEW_PERMISSION = request.form['select2___permission']
    DEF_NEW_PRIVATE = request.form['select2___private']

    # variable validation begin
    if not check_username(username=DEF_NEW_USERNAME): return error(err_msg='Geçersiz kullanıcı adı seçildi.', ret_url=RET_URL)
    if profile.query.filter(and_(profile.idProfile != get_profile.idProfile, profile.username == DEF_NEW_USERNAME)).first(): return error(err_msg='Bu kullanıcı adıyla zaten bir profil mevcut.', ret_url=RET_URL)
    # variable validation end 

    get_profile.username = DEF_NEW_USERNAME
    get_profile.password = DEF_NEW_PASSWORD
    get_profile.biography = DEF_NEW_BIOGRAPHY
    get_profile.imageAvatar = DEF_NEW_IMAGE_AVATAR
    get_profile.imageBackground = DEF_NEW_IMAGE_BACKGROUND
    get_profile.adult = DEF_NEW_ADULT
    get_profile.permission = DEF_NEW_PERMISSION
    get_profile.private = DEF_NEW_PRIVATE

    db.session.commit()

    return redirect(url_for('adminpanel_profile_edit', account_username=account_username, profile_username=DEF_NEW_USERNAME))
  # form end 

  return render_template('adminpanel/profiles/edit.html', title='Düzenleniyor: {} ({})'.format(get_profile.username, get_account.username), account_info=get_account, profile_info=get_profile, avatars_list_info=get_avatars_list, backgrounds_list_info=get_backgrounds_list)
