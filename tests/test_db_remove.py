# -*- encoding: utf-8 -*-
from includes import *



select_user_temp = profile.query.filter_by(username='ademyener').first()
select_user_temp.remove_profile()