# -*- encoding: utf-8 -*-
from includes import *

# TEST TEST TEST
@app.route('/mailxd')
def mailxd():
  try:
    msg = Message('abababababab', sender='aniwened@gmail.com', recipients=['lovisestdeus@tutanota.com'])
    msg.body = 'TEST MESAJJJJ: ' + str(request.url_root) + 'signin'
    mail.send(msg)
    return 'mail gönderildi.'
  except: return 'hata'

@app.route('/forgot-my-password', methods=['POST', 'GET'])
@app.route('/sifremi-unuttum', methods=['POST', 'GET'])
def forgotmypassword():
  if check_account() == True: return redirect(url_for('home'))
  form = ForgotMyPasswordForm()

  # GET GENERATED KEY BEGIN
  if request.args.get('key'):
    get_recovery = accountPasswordRecovery.query.filter_by(generatedKey=request.args.get('key')).first()
    if not get_recovery: return error(err_msg='Geçersiz anahtar.', ret_url=url_for('home'))
    form = NewPasswordForm()

    # NEW PASSWORD FORM BEGIN
    if form.validate_on_submit():
      if not form.new_password.data == form.new_password_confirm.data: return error(err_msg='Parolalar uyuşmuyor.', ret_url=url_for('forgotmypassword') + '?key=' + request.args.get('key'))

      get_account = account.query.filter_by(idAccount=get_recovery.idAccount).first()
      if not get_account: return error(err_msg='Bu hesap ile ilişkili anahtar bulunamadı. Yöneticiler ile iletişime geçin.', ret_url=url_for('home'))

      get_account.password = hash_str_hash(get_str=form.new_password.data)
      get_account.securityPassword = hash_str_hash(get_str=form.new_password.data)
      db.session.commit()

      get_recovery.drop()

      return error(err_msg='Parolanız başarıyla değişti!', err_code=':)', ret_url=url_for('signin'))
    # NEW PASSWORD FORM END

    return render_template('signin/newpassword.html', title='Yeni Şifrenizi Girin', form=form, header=False, footer=False)
  # GET GENERATED KEY END

  # SEND EMAIL FORM BEGIN
  if form.validate_on_submit():
    get_account = account.query.filter_by(emailAddress=form.email_address.data).first()
    if not get_account: return error(err_msg='Böyle bir hesap bulunamadı.', ret_url=url_for('forgotmypassword'))

    check_recovery = accountPasswordRecovery.query.filter_by(idAccount=get_account.idAccount).first()
    if check_recovery: return error(err_msg='Halihazırda bağlantınız gönderilmiş. E-Posta adresinizi kontrol edin.', ret_url=url_for('signin'))

    try:
      db.session.add(accountPasswordRecovery(
        idAccount = get_account.idAccount
      ))
      db.session.commit()
      msg = Message('WatchGraf - Parola Sıfırlama', sender='aniwened@gmail.com', recipients=[get_account.emailAddress])
      msg.body = 'Size özel parola yenileme bağlantınız (kimseyle paylaşmayın): ' + request.url_root + url_for('forgotmypassword') + '?key=' + accountPasswordRecovery.query.filter_by(idAccount=get_account.idAccount).first().generatedKey
      mail.send(msg)
      return error(err_msg='E-Posta adresinize yenileme bağlantısı gönderildi!', err_code=':)', ret_url=url_for('signin'))
    except: return error(err_msg='Bir hata meydana geldi.', ret_url=url_for('signin'))
  # SEND EMAIL FORM END

  return render_template('signin/forgotmypassword.html', title='Şifremi Unuttum', form=form, header=False, footer=False)

@app.route('/sign-in', methods=['POST', 'GET'])
@app.route('/giris-yap', methods=['POST', 'GET'])
def signin():
    if check_account() == True: return redirect(url_for('home'))
    form = SignInForm()
    if form.validate_on_submit():
        remember_me = False
        if 'TRUE' in request.form.getlist('remember_me'): remember_me = True

        signin_user = account.query.filter(or_(account.emailAddress == form.username.data, account.username == form.username.data)).first()
        if signin_user != None:
            # check system account
            if signin_user.permission == 'SYSTEM': return redirect(url_for('signin'))

            if hash_str_verify(get_answ=form.password.data, get_hashed_str=signin_user.password) == True:
                session['ACCOUNT'] = {
                    "idAccount": signin_user.idAccount,
                    "username": signin_user.username,
                    "password": signin_user.password,
                    "securityPassword": signin_user.securityPassword,
                    "emailAddress": signin_user.emailAddress,
                    "lastEditDate": signin_user.lastEditDate,
                    "signupDate": signin_user.signupDate
                }
                return redirect(url_for('home'))
            else: return error(err_code=':(', err_msg='Yanlış şifre girdiniz.', ret_url=url_for('signin'))
        else: return error(err_code=':(', err_msg='Böyle bir kullanıcı bulunamadı.', ret_url=url_for('signin'))
    return render_template('signin/index.html', title='Giriş Yap', form=form, header=False, footer=False)
