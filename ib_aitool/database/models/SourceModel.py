from ib_aitool.database import db

class Source(db.Model):
    __tablename__ = 'source'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(150),nullable=True,default=None)
    email=db.Column(db.VARCHAR(150),default=None)
    phone=db.Column(db.VARCHAR(150),default=None)
    url=db.Column(db.VARCHAR(150),default=None)
    datetime=db.Column(db.DateTime,default=None)
    
    def __str__(self):
        return str(self.name)

    def __init__(self, name,email,phone,url,datetime):
        self.name = name
        self.email = email
        self.phone = phone
        self.url = url
        self.datetime=datetime