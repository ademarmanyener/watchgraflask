# -*- encoding: utf-8 -*-
from includes import *

class report(db.Model):
    __tablename__ = 'report'
    idReport = ID_COLUMN(default=str(id_generator(title='report_', size=32)))
    name = STRING_COLUMN()
    emailAddress = STRING_COLUMN()
    title = STRING_COLUMN()
    message = STRING_COLUMN(size=2048, nullable=False)
    addDate = DATE_COLUMN(default=datetime.now(pytz.timezone(PY_TIMEZONE)))
    def __init__(self, name, emailAddress, title, message):
        self.idReport = str(id_generator(title='report_', size=32))
        self.name = name
        self.emailAddress = emailAddress
        self.title = title
        self.message = message
        self.addDate = datetime.now(pytz.timezone(PY_TIMEZONE))

    def drop(self):
        db.session.delete(self)
        db.session.commit()
