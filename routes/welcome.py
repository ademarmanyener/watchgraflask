# -*- encoding: utf-8 -*-
from includes import *

@app.route('/welcome', methods=['POST', 'GET'])
@app.route('/hosgeldin', methods=['POST', 'GET'])
def welcome():
    if check_account() == False: return redirect(url_for('home'))
    return render_template('welcome/index.html', title='Hoşgeldin ' + get_logged_account().username, header=False, footer=False, \
                            profile_count = profile.query.filter_by(idAccount=get_logged_account().idAccount).all())
