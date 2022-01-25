# -*- encoding: utf-8 -*-
from includes import *

"""
// functions
"""

#
# DEPRECATED! not used anymore
# use slugify instead
#
def transform_string_to_url(get_string): return get_string.lower().replace(' ', '-').replace('.', '').replace(':', '').replace("'", '')

"""
// raw sql 
"""

def sql_execute(statement): return db.engine.execute(statement)

"""
// error 
"""

def error(err_code=':(', err_msg='jus do now <-_ ->', ret_url='/'): return render_template('error/index.html', err_code=err_code, err_msg=err_msg, ret_url=ret_url, header=False, footer=False)