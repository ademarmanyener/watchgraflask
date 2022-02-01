# -*- encoding: utf-8 -*-
from includes import *

"""
// checks
"""

# beta begin
def get_logged_account():
    if current_user.is_authenticated:
        if current_user.get_class() == account:
            unique_id = current_user.idAccount
        elif current_user.get_class() == profile:
            unique_id = current_user.get_account().idAccount
        return account.query.filter_by(
            idAccount = unique_id 
        ).first()
    return None

def get_logged_profile():
    if current_user.is_authenticated:
        if current_user.get_class() == profile:
            unique_id = current_user.idProfile
        return profile.query.filter_by(
            idProfile = unique_id 
        ).first()
    return None
# beta end 

def check_account():
    if check_profile(): return True

    if current_user.is_authenticated:
        if current_user.get_class() == account:
            return True
        
    return False

def check_profile():
    if current_user.is_authenticated:
        if current_user.get_class() == profile:
            return True

    return False

def check_admin():
    if check_profile():
        if current_user.permission == 'ADMIN': return True

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