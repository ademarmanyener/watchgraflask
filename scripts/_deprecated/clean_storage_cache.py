# -*- encoding: utf-8 -*-
from import_parent import *

# since the /storage structure has been changed,
# this functions is almost completely DEPRECATED!
# DO NOT USE IT!

class WD_CacheStorage:
  DEF_STORAGE_DIR = os.path.join(os.path.dirname(app.instance_path), 'storage')

  def account(self):
    try:
      for get_account_folder_id in os.listdir(os.path.join(self.DEF_STORAGE_DIR, 'account')):
        if not account.query.filter(account.idAccount == get_account_folder_id).first():
          print('removing: {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'account', get_account_folder_id)))
          os.system('rm -rf {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'account', get_account_folder_id)))
        else:
          try:
            for get_profile_folder_id in os.listdir(os.path.join(self.DEF_STORAGE_DIR, 'account', get_account_folder_id, 'profile')):
              if not profile.query.filter(profile.idProfile == get_profile_folder_id).first():
                print('removing: {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'account', get_account_folder_id, 'profile', get_profile_folder_id)))
                os.system('rm -rf {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'account', get_account_folder_id, 'profile', get_profile_folder_id)))
          except Exception as e: print('{}'.format(e))
    except Exception as e: print('{}'.format(e))

  def collection(self):
    try:
      for get_folder_id in os.listdir(os.path.join(self.DEF_STORAGE_DIR, 'collection')):
        if not collection.query.filter(collection.idCollection == get_folder_id).first():
          print('removing: {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'collection', get_folder_id)))
          os.system('rm -rf {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'collection', get_folder_id)))
    except Exception as e: print('{}'.format(e))

  def content(self):
    try:
      for get_folder_id in os.listdir(os.path.join(self.DEF_STORAGE_DIR, 'content')):
        if not content.query.filter(content.idContent == get_folder_id).first():
          print('removing: {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'content', get_folder_id)))
          os.system('rm -rf {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'content', get_folder_id)))
        else:
          if 'season' in os.listdir(os.path.join(self.DEF_STORAGE_DIR, 'content', get_folder_id)):
            try:
              for get_season_folder_id in os.listdir(os.path.join(self.DEF_STORAGE_DIR, 'content', get_folder_id, 'season')):
                if not tvSeasonContent.query.filter(tvSeasonContent.idTvSeason == get_season_folder_id).first():
                  print('removing: {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'content', get_folder_id, 'season', get_season_folder_id)))
                  os.system('rm -rf {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'content', get_folder_id, 'season', get_season_folder_id)))
                else:
                  if 'episode' in os.listdir(os.path.join(self.DEF_STORAGE_DIR, 'content', get_folder_id, 'season', get_season_folder_id)):
                    try:
                      for get_episode_folder_id in os.listdir(os.path.join(self.DEF_STORAGE_DIR, 'content', get_folder_id, 'season', get_season_folder_id, 'episode')):
                        if not tvEpisodeContent.query.filter(tvEpisodeContent.idTvEpisode == get_episode_folder_id).first():
                          print('removing: {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'content', get_folder_id, 'season', get_season_folder_id, 'episode', get_episode_folder_id)))
                          os.system('rm -rf {}'.format(os.path.join(self.DEF_STORAGE_DIR, 'content', get_folder_id, 'season', get_season_folder_id, 'episode', get_episode_folder_id)))
                    except Exception as e: print('{}'.format(e))
            except Exception as e: print('{}'.format(e))
    except Exception as e: print('{}'.format(e))

  def __init__(self, account=True, collection=True, content=True):
    if account: self.account()
    if collection: self.collection()
    if content: self.content()

WD_CacheStorage()
