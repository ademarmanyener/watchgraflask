# -*- encoding: utf-8 -*-
from includes import *

@app.route('/message/test')
@app.route('/mesaj/test')
def message_test():
  if not check_admin(): return redirect(url_for('home'))

  return render_template('message/test.html')
