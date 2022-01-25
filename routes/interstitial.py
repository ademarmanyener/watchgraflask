# -*- encoding: utf-8 -*-
from includes import *

@app.route('/interstitial', methods=['POST', 'GET'])
@app.route('/gecis-reklami', methods=['POST', 'GET'])
def interstitial():
    ret_url = url_for('home')
    if request.args.get('ret_url'): ret_url = request.args.get('ret_url')
    return render_template('interstitial/index.html', title="Geçiş Reklamı", header=False, footer=False, ret_url=ret_url)
