# -*- encoding: utf-8 -*-
from includes import *

@app.route('/contact', methods=['POST', 'GET'])
@app.route('/iletisim', methods=['POST', 'GET'])
def contact():
  if check_account() and not check_profile(): return redirect(url_for('whoiswatching'))

  form = ContactForm()

  # SEND EMAIL FORM BEGIN
  if form.validate_on_submit():
    try:
      msg = Message('WatchGraf - İletişim - {}'.format(form.title.data), sender='aniwened@gmail.com', recipients=['watchgraf@pm.me'])
      msg.body = '{} ({}) tarafından gönderildi. İçerik: {}.'.format(form.name.data, form.email_address.data, form.message.data)
      mail.send(msg)
      return error(err_msg='Bizimle iletişime geçtiğiniz için teşekkür ederiz!', err_code=':)', ret_url=url_for('contact'))
    except:
        try:
            db.session.add(report(
                name = form.name.data,
                emailAddress = form.email_address.data,
                title = form.title.data,
                message = form.message.data,
            ))
            db.session.commit()
            return redirect(url_for('contact')) 
        except: return error(err_msg='Bir hata meydana geldi.', ret_url=url_for('contact'))
  # SEND EMAIL FORM END

  return render_template('contact/index.html', title='İletişim', form=form)
