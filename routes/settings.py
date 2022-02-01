# -*- encoding: utf-8 -*-
from includes import *

#### W.I.P. for Settings Account Page

# account settings page
@app.route('/settings/account', methods=['POST', 'GET'])
@app.route('/ayarlar/hesap', methods=['POST', 'GET'])
def settings_account_confirm_enter():
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    get_account = account.query.filter_by(idAccount=get_logged_account().idAccount).first()
    if get_account == None: return error(err_msg='Böyle bir hesap bulunamadı.', ret_url=url_for('whoiswatching'))

    confirmenterform = SettingsAccountConfirmEnterForm()

    if confirmenterform.validate_on_submit():
        if hash_str_verify(get_answ=confirmenterform.security_password.data, get_hashed_str=get_account.securityPassword) == True:
            return settings_account()
        else: return error(err_msg='Güvenlik parolanızı yanlış girdiniz.', ret_url=url_for('settings_account_confirm_enter'))
    return render_template('settings/account_confirm_enter.html', title='Hesap Ayarları - Güvenlik Şifrenizi Girin', header=False, footer=False, \
                                                                  select_account=get_account, \
                                                                  confirmenterform=confirmenterform)

# account settings page
def settings_account():
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    #get_account = account.query.filter_by(idAccount=get_logged_account().idAccount).first()
    #if get_account == None: return error(err_msg='Böyle bir hesap bulunamadı.', ret_url=url_for('whoiswatching'))

    changemyusernameemailform = SettingsAccountChangeUsernameEmailForm()
    changemypasswordform = SettingsAccountChangePasswordForm()
    changemysecuritypasswordform = SettingsAccountChangeSecurityPasswordForm()

    return render_template('settings/account.html', title='Hesap Ayarları', header=False, footer=False, \
                                                    changemyusernameemailform=changemyusernameemailform, \
                                                    changemypasswordform=changemypasswordform, \
                                                    changemysecuritypasswordform=changemysecuritypasswordform)

# drop account confirmation
@app.route('/settings/account/dropaccount/confirmation', methods=['POST', 'GET'])
@app.route('/ayarlar/hesap/hesabisil/onay', methods=['POST', 'GET'])
def settings_account_dropaccount_confirmation():
  if check_account() == False: return redirect(url_for('home'))

  ret_url = url_for('home')

  select_account = account.query.filter_by(idAccount=get_logged_account().idAccount).first()
  if select_account == None: return error(err_msg="Couldn't find such an account.", ret_url=ret_url)

  form = SettingsAccountDropAccountConfirmationForm()
  if form.validate_on_submit():
    if hash_str_verify(get_answ=form.password.data, get_hashed_str=select_account.password) == True:
      select_account.drop()
      return redirect(url_for('destroy_account'))
    else: return error(err_msg='Yanlış hesap şifresi girdiniz!', ret_url=url_for('settings_account_dropaccount_confirmation'))
  return render_template('settings/dropaccount/confirmation.html', title='Parola Doğrulaması ile Hesabı Sil', header=False, footer=False, select_account=select_account, form=form)

@app.route('/settings/account/func/<function>/proc', methods=['POST'])
def settings_account_func_proc(function):
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    if request.is_json == False: return error(err_msg='JSON değil.')

    get_account = account.query.filter_by(idAccount=get_logged_account().idAccount).first()
    if get_account == None: return error(err_msg='Böyle bir hesap bulunamadı.', ret_url=url_for('home'))

    if function == 'change_username_emailaddress':
        get_new_username = request.get_json()['new_username']
        get_new_email_address = request.get_json()['new_email_address']

        ## validation
        if check_username(username=get_new_username) == False or check_email_address(email_address=get_new_email_address) == False: return make_response(jsonify({'err_msg': 'Kullanıcı & E-posta geçersiz girildi.'}))

        ## if the username was changed
        if get_new_username != get_account.username:
            if account.query.filter_by(username=get_new_username).first() != None: return make_response(jsonify({'err_msg': 'Bu kullanıcı adı zaten başka bir hesap tarafından kullanılmakta.'}))
            else: get_account.username = get_new_username
        ## if the email address was changed
        if get_new_email_address != get_account.emailAddress:
            if account.query.filter_by(emailAddress=get_new_email_address).first() != None: return make_response(jsonify({'err_msg': 'Bu e-posta adresi zaten başka bir hesap tarafından kullanılmakta.'}))
            else: get_account.emailAddress = get_new_email_address
        db.session.commit()
        return make_response(jsonify({'succ_msg': 'Kullanıcı & E-Posta adresiniz başarıyla güncellendi!'}))

    if function == 'change_password':
        get_current_password = request.get_json()['current_password']
        get_new_password = request.get_json()['new_password']
        get_confirm_new_password = request.get_json()['confirm_new_password']

        ## validation
        if len(get_new_password) < 12 or len(get_confirm_new_password) < 12: return make_response(jsonify({'err_msg': 'Parola karakterini yeterince uzun girmediniz.'}))

        if hash_str_verify(get_answ=get_current_password, get_hashed_str=get_account.password) == True:
            if get_new_password == get_confirm_new_password:
                get_account.password = hash_str_hash(get_str=get_new_password)
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'Parolanız başarıyla güncellendi!'}))
            else: return make_response(jsonify({'err_msg': 'Yeni parolalar uyuşmuyor.'}))
        else: return make_response(jsonify({'err_msg': 'Eski parolanızı yanlış girdiniz.'}))

    if function == 'change_security_password':
        get_current_security_password = request.get_json()['current_security_password']
        get_new_security_password = request.get_json()['new_security_password']
        get_confirm_new_security_password = request.get_json()['confirm_new_security_password']

        ## validation
        if len(get_new_security_password) < 12 or len(get_confirm_new_security_password) < 12: return make_response(jsonify({'err_msg': 'Parola karakterini yeterince uzun girmediniz.'}))

        if hash_str_verify(get_answ=get_current_security_password, get_hashed_str=get_account.securityPassword) == True:
            if get_new_security_password == get_confirm_new_security_password:
                get_account.securityPassword = hash_str_hash(get_str=get_new_security_password)
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'Güvenlik parolanız başarıyla güncellendi!'}))
            else: return make_response(jsonify({'err_msg': 'Yeni güvenlik parolaları uyuşmuyor.'}))
        else: return make_response(jsonify({'err_msg': 'Eski güvenlik parolanızı yanlış girdiniz.'}))

@app.route('/settings/profile/func/<function>/proc', methods=['POST'])
def settings_profile_func_proc(function):
    if check_account() == False: return redirect(url_for('home'))
    if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

    if request.is_json == False: return error(err_msg='JSON değil.')

    get_profile = profile.query.filter(and_(profile.idAccount == get_logged_account().idAccount, profile.idProfile == get_logged_profile().idProfile)).first()
    if get_profile == None: return error(err_msg='Böyle bir profil bulunamadı.', ret_url=url_for('whoiswatching'))

    if function == 'change_username':
        get_new_username = request.get_json()['new_username']
        if get_new_username:
            if check_username(username=get_new_username) == False: return make_response(jsonify({'err_msg': 'Kullanıcı adında geçersiz karakterler mevcut!'}))
            check_if_exists = profile.query.filter(and_(profile.idAccount == get_logged_account().idAccount, profile.username == get_new_username)).first()
            if check_if_exists != None: return make_response(jsonify({'err_msg': 'Bu kullanıcı adı zaten bir profil tarafından kullanılmaktadır!'}))
            get_profile.username = get_new_username
            db.session.commit()
            return make_response(jsonify({'succ_msg': 'Kullanıcı adınız başarıyla değiştirildi!'}))
        else: return make_response(jsonify({'err_msg': 'Kullanıcı adı boş bırakılamaz!'}))
    if function == 'change_password':
        get_current_password = request.get_json()['current_password']
        get_new_password = request.get_json()['new_password']
        get_confirm_new_password = request.get_json()['confirm_new_password']

        if get_profile.password == get_current_password:
            if get_new_password == get_confirm_new_password:
                get_profile.password = get_new_password
                db.session.commit()
                return make_response(jsonify({'succ_msg': 'Parolanız başarıyla değiştirildi!'}))
            else: return make_response(jsonify({'err_msg': 'Yeni parolaların eşleştiğine emin misiniz?'}))
        else: return make_response(jsonify({'err_msg': 'Mevcut parolanızı doğru girdiğinize emin misiniz?'}))

    if function == 'make_private_false':
        get_profile.private = False
        db.session.commit()
        return make_response(jsonify({'succ_msg': 'OKEE!'}))
    if function == 'make_private_true':
        get_profile.private = True
        db.session.commit()
        return make_response(jsonify({'succ_msg': 'OKEE2!'}))
    if function == 'make_adult_false':
        get_profile.adult = False
        db.session.commit()
        return make_response(jsonify({'succ_msg': 'OKEE3!'}))
    if function == 'make_adult_true':
        get_profile.adult = True
        db.session.commit()
        return make_response(jsonify({'succ_msg': 'OKEE4!'}))

    db.session.commit()

    return make_response(jsonify({'ret_url': url_for('settings_profile')}))

@app.route('/settings/profile', methods=['POST', 'GET'])
@app.route('/ayarlar/profil', methods=['POST', 'GET'])
def settings_profile():
  if not check_profile(): return redirect(url_for('whoiswatching'))

  #if not check_admin(): return error(err_msg='Bu sayfa bakımdadır.')

  RET_URL = url_for('settings_profile')

  get_account = account.query.filter(account.idAccount == get_logged_account().idAccount).first()
  if not get_account: return error(err_msg='Böyle bir hesap bulunamadı.', ret_url=url_for('signin'))

  get_profile = profile.query.filter(and_(profile.idProfile == get_logged_profile().idProfile, profile.idAccount == get_logged_account().idAccount)).first()
  if not get_profile: return error(err_msg='Böyle bir profil bulunamadı.', ret_url=url_for('whoiswatching'))

  """
  try:
    get_avatars_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'account', get_account.idAccount, 'profile', get_profile.idProfile, 'avatar'))
    get_backgrounds_list = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'storage', 'account', get_account.idAccount, 'profile', get_profile.idProfile, 'background'))
  except:
    get_avatars_list = ''
    get_backgrounds_list = ''
  """

  # form begin
  if request.method == 'POST':
    # check if a file is uploaded
    uploadFile_imageAvatar = request.files['form__img-upload']
    uploadFile_imageBackground = request.files['form__imgBg-upload']
    if uploadFile_imageAvatar:
      CustomFormComponent.upload_file(upload_file=uploadFile_imageAvatar, save_folder_path=os.path.join(app.root_path, 'storage', 'profile', get_profile.idProfile), file_type='avatar')
      get_profile.imageAvatar = '/storage/profile/{}/avatar.jpg'.format(get_profile.idProfile)
    if uploadFile_imageBackground:
      CustomFormComponent.upload_file(upload_file=uploadFile_imageBackground, save_folder_path=os.path.join(app.root_path, 'storage', 'profile', get_profile.idProfile), file_type='background')
      get_profile.imageBackground = '/storage/profile/{}/background.jpg'.format(get_profile.idProfile)

    #DEF_NEW_USERNAME = request.form['input___username']
    DEF_NEW_BIOGRAPHY = request.form['input___biography']
    # IMAGE UPLOAD BEGIN
    """
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
    """
    # IMAGE UPLOAD END

    # variable validation begin
    #if not check_username(username=DEF_NEW_USERNAME): return error(err_msg='Geçersiz kullanıcı adı seçildi.', ret_url=RET_URL)
    #if profile.query.filter(and_(profile.idProfile != get_profile.idProfile, profile.username == DEF_NEW_USERNAME)).first(): return error(err_msg='Bu kullanıcı adıyla zaten bir profil mevcut.', ret_url=RET_URL)
    # variable validation end

    #get_profile.username = DEF_NEW_USERNAME
    get_profile.biography = DEF_NEW_BIOGRAPHY
    #get_profile.imageAvatar = DEF_NEW_IMAGE_AVATAR
    #get_profile.imageBackground = DEF_NEW_IMAGE_BACKGROUND

    db.session.commit()

    return redirect(url_for('settings_profile'))
  # form end

  #return render_template('settings/profile.html', title=get_profile.username + ' Profil Ayarları', account_info=get_account, profile_info=get_profile, avatars_list_info=get_avatars_list, backgrounds_list_info=get_backgrounds_list)
  return render_template('settings/profile.html', title='{} Profil Ayarları'.format(get_profile.username), context = {
                                                                                                              'profile': get_profile,
                                                                                                              'account': get_account,
                                                                                                            })

# drop profile confirmation
@app.route('/settings/profile/dropprofile/confirmation', methods=['POST', 'GET'])
@app.route('/ayarlar/profil/profilisil/onay', methods=['POST', 'GET'])
def settings_profile_dropprofile_confirmation():
  if check_account() == False: return redirect(url_for('home'))
  if check_account() == True and check_profile() == False: return redirect(url_for('whoiswatching'))

  ret_url = url_for('home')

  select_account = account.query.filter_by(idAccount=get_logged_account().idAccount).first()
  if select_account == None: return error(err_msg="Couldn't find such an account.", ret_url=ret_url)

  select_profile = profile.query.filter(and_(profile.idAccount == get_logged_account().idAccount, profile.idProfile == get_logged_profile().idProfile)).first()
  if select_profile == None: return error(err_msg="Couldn't find such an profile.", ret_url=ret_url)

  form = SettingsProfileDropProfileConfirmationForm()
  if form.validate_on_submit():
    if hash_str_verify(get_answ=form.password.data, get_hashed_str=select_account.password) == True:
      select_profile.drop()
      return redirect(url_for('destroy_profile'))
    else: return error(err_msg='Yanlış hesap şifresi girdiniz!', ret_url=url_for('settings_profile_dropprofile_confirmation'))
  return render_template('settings/dropprofile/confirmation.html', title='Parola Doğrulaması ile Profili Sil', header=False, footer=False, select_account=select_account, select_profile=select_profile, form=form)
