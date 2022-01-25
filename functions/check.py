# -*- encoding: utf-8 -*-
from includes import *

"""
// checks
"""

def check_account():
    if 'ACCOUNT' in session:
        return True
    return False

def check_profile():
    if check_account() == True:
        if 'PROFILE' in session:
            return True
    return False

def check_admin():
    if check_account() == True:
        if check_profile() == True:
            get_profile = profile.query.filter(and_(profile.idProfile == session['PROFILE']['idProfile'], profile.idAccount == session['ACCOUNT']['idAccount'])).first()
            if not get_profile: return 1
            if get_profile.permission == 'ADMIN':
                return True
    return False

def check_email_address(email_address):
  regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
  if re.search(regex, email_address): return True
  else: return False

def check_username(username):
    result = True
    if is_restricted(username=username.lower()): result = False
    if len(username) <= 2 or len(username) >= 18: result = False
    else:
        for letter in username:
            if letter not in string.ascii_lowercase + string.digits + '_': result = False
    return result

# IT'S ABOUT TO GET DEPRECATED.
def check_follow(follower_account_id, follower_profile_id, following_account_id, following_profile_id):
    result = True
    check_follow = follow.query.filter(and_(follow.idFollowerAccount == follower_account_id, follow.idFollowerProfile == follower_profile_id, follow.idFollowingAccount == following_account_id, follow.idFollowingProfile == following_profile_id)).first()
    if check_follow == None: result = None
    return result