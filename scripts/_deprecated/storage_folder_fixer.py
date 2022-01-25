# -*- encoding: utf-8 -*-
from import_parent import *

class StorageFolderFixer:
    STORAGE_FOLDER_PATH = ''
    def __init__(self):
        self.STORAGE_FOLDER_PATH = os.path.join(app.root_path, 'storage')

    class Template:
        TEMPLATE_FOLDER_PATH = ''
        def __init__(self):
            self.TEMPLATE_FOLDER_PATH = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'template')

        # for each `row` check folder
        # if doesn't exist then CREATE
        def create(self): return 1

        # for each folder check `row` 
        # if doesn't exist then REMOVE 
        def remove(self): return 1

    def run_all(self):
        self.Content().create()
        self.Content().remove()
        self.Profile().create()
        self.Profile().remove()
        self.Cast().create()
        self.Cast().remove()
        self.Collection().create()
        self.Collection().remove()

    class Content:
        CONTENT_FOLDER_PATH = ''
        def __init__(self):
            self.CONTENT_FOLDER_PATH = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'content')

        def create(self):
            print(' ==> ' + type(StorageFolderFixer.STORAGE_FOLDER_PATH))
            for _content in content.query.all():
                _tmp_folderPath = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'content', _content.idContent)
                #print(_tmp_folderPath)
                """
                if not os.path.isdir(_tmp_folderPath):
                    os.makedirs(_tmp_folderPath)
                    print('[+] created folder: {}'.format(_tmp_folderPath))
                """

        def remove(self):
            for _folder in os.listdir(os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'content')):
                if not content.query.filter_by(idContent=_folder).first():
                    _tmp_folderPath = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'content', _folder)
                    os.removedirs(_tmp_folderPath)
                    print('[-] removed folder: {}'.format(_tmp_folderPath))

    class Profile:
        PROFILE_FOLDER_PATH = ''
        def __init__(self):
            self.PROFILE_FOLDER_PATH = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'profile')

        def create(self):
            for _profile in profile.query.all():
                _tmp_folderPath = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'profile', _profile.idProfile)
                if not os.path.isdir(_tmp_folderPath):
                    os.makedirs(_tmp_folderPath)
                    print('[+] created folder: {}'.format(_tmp_folderPath))

        def remove(self):
            for _folder in os.listdir(os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'profile')):
                if not profile.query.filter_by(idProfile=_folder).first():
                    _tmp_folderPath = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'profile', _folder)
                    os.removedirs(_tmp_folderPath)
                    print('[-] removed folder: {}'.format(_tmp_folderPath))

    class Cast:
        CAST_FOLDER_PATH = ''
        def __init__(self):
            self.CAST_FOLDER_PATH = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'cast')

        def create(self):
            for _cast in cast.query.all():
                _tmp_folderPath = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'cast', _cast.idCast)
                if not os.path.isdir(_tmp_folderPath):
                    os.makedirs(_tmp_folderPath)
                    print('[+] created folder: {}'.format(_tmp_folderPath))

        def remove(self):
            for _folder in os.listdir(os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'cast')):
                if not cast.query.filter_by(idCast=_folder).first():
                    _tmp_folderPath = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'cast', _folder)
                    os.removedirs(_tmp_folderPath)
                    print('[-] removed folder: {}'.format(_tmp_folderPath))

    class Collection:
        COLLECTION_FOLDER_PATH = ''
        def __init__(self):
            self.COLLECTION_FOLDER_PATH = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'collection')

        def create(self):
            for _collection in collection.query.all():
                #_tmp_folderPath = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'collection', _collection.idCollection)
                _tmp_folderPath = os.path.join(self.COLLECTION_FOLDER_PATH, _collection.idCollection)
                #print('\t\tdebug: {}'.format(_tmp_folderPath))
                if not os.path.isdir(_tmp_folderPath):
                    os.makedirs(_tmp_folderPath)
                    print('[+] created folder: {}'.format(_tmp_folderPath))

        def remove(self):
            for _folder in os.listdir(os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'collection')):
                if not collection.query.filter_by(idCollection=_folder).first():
                    _tmp_folderPath = os.path.join(StorageFolderFixer.STORAGE_FOLDER_PATH, 'collection', _folder)
                    os.removedirs(_tmp_folderPath)
                    print('[-] removed folder: {}'.format(_tmp_folderPath))

# i think i found the solution
class StorageFolderFixer2:
    def __init__(self):
        get_folder = os.path.join(app.root_path, 'storage', 'content')
        for _folder in os.listdir(get_folder):
            if not content.query.filter_by(idContent=_folder).first():
                os.removedirs(os.path.join(app.root_path, 'storage', 'content', _folder))
                print(' ==> removed: {}'.format(_folder))

if __name__ == '__main__': StorageFolderFixer().run_all()
#if __name__ == '__main__': StorageFolderFixer2()