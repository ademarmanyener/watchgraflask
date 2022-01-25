# -*- encoding: utf-8 -*-
from includes import *

@app.route('/report')
@app.route('/hatabildir')
def report_beta():
  return render_template('report/index.html')
