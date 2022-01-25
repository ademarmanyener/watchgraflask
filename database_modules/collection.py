# -*- encoding: utf-8 -*-
from includes import *

class collection(db.Model):
    __tablename__ = 'collection'
    idCollection = ID_COLUMN(default=str(id_generator(title='collection_', size=32)))
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    title = STRING_COLUMN()
    titleUrl = STRING_COLUMN()
    overview = STRING_COLUMN()
    private = INTEGER_COLUMN(default=0)
    imagePoster = STRING_COLUMN(size=2048, nullable=True)
    imageBackground = STRING_COLUMN(size=2048, nullable=True) # ! BETA
    recommended = INTEGER_COLUMN(nullable=True) # ! BETA
    lastEditDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idAddProfile, idAddAccount, title, titleUrl, overview, private, imagePoster, imageBackground, recommended, lastEditDate):
        self.idCollection = str(id_generator(title='collection_', size=32))
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount 
        self.title = title 
        self.titleUrl = titleUrl
        self.overview = overview
        self.private = private
        self.imagePoster = imagePoster
        self.imageBackground = imageBackground
        self.recommended = recommended
        self.lastEditDate = lastEditDate
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

        #### FOLDER
        collection_dir = os.path.join(STORAGE_PATH, 'collection', self.idCollection)
        #poster_dir = os.path.join(collection_dir, 'poster')
        #background_dir = os.path.join(collection_dir, 'background')

        # mkdir: /storage/collection/{{idCollection}}
        if not os.path.exists(collection_dir): os.makedirs(collection_dir)

        # mkdir: /storage/collection/{{idCollection}}/poster
        #if not os.path.exists(poster_dir): os.makedirs(poster_dir)

        # mkdir: /storage/collection/{{idCollection}}/background
        #if not os.path.exists(background_dir): os.makedirs(background_dir)
        #### END FOLDER
    
    def drop(self):
        #### FOLDER
        collection_dir = os.path.join(STORAGE_PATH, 'collection', self.idCollection)
        os.system('rm -rf ' + collection_dir)
        #### END FOLDER

        for get_collection_tag in collectionTag.query.filter_by(idCollection=self.idCollection).all():
            get_collection_tag.drop()

        for get_collection_item in collectionItem.query.filter_by(idCollection=self.idCollection).all():
            get_collection_item.drop()

        db.session.delete(self)
        db.session.commit()

class collectionTag(db.Model):
    __tablename__ = 'collectiontag'
    idTag = ID_COLUMN(default=str(id_generator(title='collection_tag_', size=32)))
    idCollection = ID_COLUMN(foreign_key='collection.idCollection')
    title = STRING_COLUMN()
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idCollection, title):
        self.idTag = str(id_generator(title='collection_tag_', size=32))
        self.idCollection = idCollection 
        self.title = title
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()

class collectionItem(db.Model):
    __tablename__ = 'collectionitem'
    idItem = ID_COLUMN(default=str(id_generator(title='collection_item_', size=32)))
    idCollection = ID_COLUMN(foreign_key='collection.idCollection')
    idAddProfile = ID_COLUMN(foreign_key='profile.idProfile')
    idAddAccount = ID_COLUMN(foreign_key='account.idAccount')
    idContent = ID_COLUMN(foreign_key='content.idContent')
    index = INTEGER_COLUMN()
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, idCollection, idAddProfile, idAddAccount, idContent):
        self.idItem = str(id_generator(title='collection_item_', size=32))
        self.idCollection = idCollection 
        self.idAddProfile = idAddProfile
        self.idAddAccount = idAddAccount 
        self.idContent = idContent
        self.index = 0 # index starts from 0, it goes upper it goes topper. pretty easy right?
        self.addDate = datetime.now()

    def drop(self):
        db.session.delete(self)
        db.session.commit()
