from ib_aitool.database import db
class CandidateScore(db.Model):
    __tablename__ = 'candidates_score'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer,default=None,nullable=False)
    candidate_id=db.Column(db.Integer,default=None,nullable=False)
    modified_by=db.Column(db.Integer,default=None,nullable=False)
    score=db.Column(db.Text,default=None,nullable=True)
    score_desc=db.Column(db.Text,default=None,nullable=True)
    status=db.Column(db.Enum("0","1"),default=0,nullable=False)
    datetime=db.Column(db.DateTime,default=None)
    
    def __str__(self):
        return str(self.name)

    def __init__(self, profile_id,candidate_id,modified_by,score,score_desc,status,datetime):
        self.name = name
        self.profile_id = profile_id
        self.candidate_id = candidate_id
        self.modified_by = modified_by
        self.score=score
        self.score_desc=score_desc
        self.status=status
        self.datetime = datetime