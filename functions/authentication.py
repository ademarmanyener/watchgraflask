# -*- encoding: utf-8 -*-
from includes import *

"""

// authentication codes here

"""

@app.before_request
def before_request():
  # beta begin
  if SETTINGS['debug']['enabled']:
    get_debug_account = account.query.filter_by(username=SETTINGS['debug']['session']['account_username']).first()
    if get_debug_account:
      get_debug_profile = profile.query.filter_by(username=SETTINGS['debug']['session']['profile_username'], idAccount=get_debug_account.idAccount).first()
      session['ACCOUNT'] = {'idAccount': get_debug_account.idAccount}
      session['PROFILE'] = {'idProfile': get_debug_profile.idProfile}
  # beta end 
  g.AVATARS_LIST = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'static', 'img', 'avatars'))
  g.BACKGROUNDS_LIST = os.listdir(os.path.join(os.path.dirname(app.instance_path), 'static', 'img', 'backgrounds'))
  if 'ACCOUNT' in session: g.ACCOUNT = session['ACCOUNT']
  if 'PROFILE' in session:
    g.PROFILE = session['PROFILE']
    g.PROFILE_COLLECTIONS_LIST = collection.query.filter(and_(collection.idAddProfile == session['PROFILE']['idProfile'], collection.idAddAccount == session['ACCOUNT']['idAccount'])).order_by(collection.addDate.desc()).all()

@app.route('/destroy_account/' + str(id_generator(size=256)))
def destroy_account():
    session.pop('ACCOUNT', None)
    session.pop('PROFILE', None)
    return redirect(url_for('home'))

@app.route('/destroy_profile/' + str(id_generator(size=256)))
def destroy_profile():
    session.pop('PROFILE', None)
    return redirect(url_for('whoiswatching'))
