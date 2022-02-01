# -*- encoding: utf-8 -*-
from includes import *

@app.route('/sign-up', methods=['POST', 'GET'])
@app.route('/kayit-ol', methods=['POST', 'GET'])
def signup():
    if check_account() == True: return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        if not profile.query.filter_by(permission='DOCKER').first(): return redirect(url_for('init_login'))

        if check_username(username=form.username.data) == False: return error(err_msg='Kullanıcı adında geçersiz karakterler mevcut.', ret_url=url_for('signup'))

        check_user = account.query.filter(or_(account.username == form.username.data, account.emailAddress == form.email_address.data)).first()
        if check_user != None: return error(err_msg='Bu kullanıcı adı/email ile zaten kayıt olunmuş.', ret_url=url_for('signup'))

        check_privacy_policy = False
        if request.form.getlist('privacypolicy'): check_privacy_policy = True
        if check_privacy_policy == False: return error(err_msg='Sözleşmeyi kabul etmediniz.', ret_url=url_for('signup'))

        db.session.add(account(
            username = form.username.data,
            password = hash_str_hash(get_str=form.password.data),
            securityPassword = hash_str_hash(get_str=form.password.data),
            emailAddress = form.email_address.data,
            permission = 'USER',
            lastEditDate = datetime.now()
        ))
        db.session.commit()

        signup_account = account.query.filter_by(username = form.username.data).first()
        if signup_account != None:
            if request.args.get('ref'):
                check_ref_account = account.query.filter_by(idAccount = request.args.get('ref')).first()
                if check_ref_account != None:
                    db.session.add(reference(
                        idGuestAccount = signup_account.idAccount,
                        idHostAccount = request.args.get('ref')
                    ))
                    db.session.commit()
            session['login_type'] = 'ACCOUNT'
            login_user(signup_account)
            return redirect(url_for('home'))
        else: return error(err_msg='Bir hata meydana geldi.', ret_url=url_for('signup'))
    return render_template('signup/index.html', title='Kayıt Ol', form=form, header=False, footer=False)
