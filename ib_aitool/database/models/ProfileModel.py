from ib_aitool.database import db
class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    uploaded_by = db.Column(db.Integer,nullable=False,default=None)
    title=db.Column(db.VARCHAR(50),default=None)
    roles_responsibilities=db.Column(db.Text,default=None)
    additional_skills=db.Column(db.Text,default=None)
    key_skills=db.Column(db.Text,default=None)
    experience_from=db.Column(db.VARCHAR(20),default=None)
    experience_to=db.Column(db.VARCHAR(20),default=None)
    status=db.Column(db.Enum("0","1"),default=None)
    openings=db.Column(db.VARCHAR(20),default=None)
    datetime=db.Column(db.DateTime,default=None)
    
    def __str__(self):
        return str(self.name)

    def __init__(self, uploaded_by,title,roles_responsibilities,additional_skills,experience_from,experience_to,status,openings,datetime):
        self.name = name
        self.uploaded_by = uploaded_by
        self.roles_responsibilities = roles_responsibilities
        self.additional_skills = additional_skills
        self.experience_from=experience_from
        self.experience_to=experience_to
        self.status=status
        self.openings=openings
        self.datetime = datetime