# -*- encoding: utf-8 -*-
from import_parent import *
from termcolor import colored
import shutil

class StorageFolderFixer:
    STORAGE_FOLDER_PATH = os.path.join(app.root_path, 'storage')

    def __init__(self):
        self.content = self.Content(path=os.path.join(self.STORAGE_FOLDER_PATH, 'content'))
        self.profile = self.Profile(path=os.path.join(self.STORAGE_FOLDER_PATH, 'profile'))
        self.cast = self.Cast(path=os.path.join(self.STORAGE_FOLDER_PATH, 'cast'))
        self.collection = self.Collection(path=os.path.join(self.STORAGE_FOLDER_PATH, 'collection'))
        self.content.create()
        self.content.remove()
        self.profile.create()
        self.profile.remove()
        self.cast.create()
        self.cast.remove()
        self.collection.create()
        self.collection.remove()

    class Content:
        def __init__(self, path):
            self.CONTENT_FOLDER_PATH = path

        def create(self):
            for _content in content.query.all():
                if not os.path.isdir(os.path.join(self.CONTENT_FOLDER_PATH, _content.idContent)):
                    os.makedirs(os.path.join(self.CONTENT_FOLDER_PATH, _content.idContent))
                    print(colored(' [+]', 'green', attrs=['bold']), colored('[CONTENT]', attrs=['bold']), 'created:', colored(_content.title, attrs=['bold']))

        def remove(self):
            for _folder in os.listdir(self.CONTENT_FOLDER_PATH):
                if not content.query.filter_by(idContent=_folder).first():
                    shutil.rmtree(os.path.join(self.CONTENT_FOLDER_PATH, _folder))
                    print(colored(' [✘]', 'red', attrs=['bold']), colored('[CONTENT]', attrs=['bold']), 'removed:', colored(_folder, attrs=['bold']))

    class Profile:
        def __init__(self, path):
            self.PROFILE_FOLDER_PATH = path

        def create(self):
            for _profile in profile.query.all():
                if not os.path.isdir(os.path.join(self.PROFILE_FOLDER_PATH, _profile.idProfile)):
                    os.makedirs(os.path.join(self.PROFILE_FOLDER_PATH, _profile.idProfile))
                    print(colored(' [+]', 'green', attrs=['bold']), colored('[PROFILE]', attrs=['bold']), 'created:', colored(_profile.username, attrs=['bold']))

        def remove(self):
            for _folder in os.listdir(self.PROFILE_FOLDER_PATH):
                if not profile.query.filter_by(idProfile=_folder).first():
                    shutil.rmtree(os.path.join(self.PROFILE_FOLDER_PATH, _folder))
                    print(colored(' [✘]', 'red', attrs=['bold']), colored('[PROFILE]', attrs=['bold']), 'removed:', colored(_folder, attrs=['bold']))

    class Cast:
        def __init__(self, path):
            self.CAST_FOLDER_PATH = path

        def create(self):
            for _cast in cast.query.all():
                if not os.path.isdir(os.path.join(self.CAST_FOLDER_PATH, _cast.idCast)):
                    os.makedirs(os.path.join(self.CAST_FOLDER_PATH, _cast.idCast))
                    print(colored(' [+]', 'green', attrs=['bold']), colored('[CAST]', attrs=['bold']), 'created:', colored(_cast.name, attrs=['bold']))

        def remove(self):
            for _folder in os.listdir(self.CAST_FOLDER_PATH):
                if not cast.query.filter_by(idCast=_folder).first():
                    shutil.rmtree(os.path.join(self.CAST_FOLDER_PATH, _folder))
                    print(colored(' [✘]', 'red', attrs=['bold']), colored('[CAST]', attrs=['bold']), 'removed:', colored(_folder, attrs=['bold']))

    class Collection:
        def __init__(self, path):
            self.COLLECTION_FOLDER_PATH = path

        def create(self):
            for _collection in collection.query.all():
                if not os.path.isdir(os.path.join(self.COLLECTION_FOLDER_PATH, _collection.idCollection)):
                    os.makedirs(os.path.join(self.COLLECTION_FOLDER_PATH, _collection.idCollection))
                    print(colored(' [+]', 'green', attrs=['bold']), colored('[COLLECTION]', attrs=['bold']), 'created:', colored(_collection.title, attrs=['bold']))

        def remove(self):
            for _folder in os.listdir(self.COLLECTION_FOLDER_PATH):
                if not collection.query.filter_by(idCollection=_folder).first():
                    shutil.rmtree(os.path.join(self.COLLECTION_FOLDER_PATH, _folder))
                    print(colored(' [✘]', 'red', attrs=['bold']), colored('[COLLECTION]', attrs=['bold']), 'removed:', colored(_folder, attrs=['bold']))

StorageFolderFixer()
