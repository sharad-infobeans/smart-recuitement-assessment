from ib_aitool.database import db
from ib_aitool.database.models.User import User
from flask_login import current_user

class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False,default=None)
    interview_video = db.Column(db.Text,default=None)
    interview_audio = db.Column(db.Text,default=None)
    is_report_generated = db.Column(db.Boolean,default=False)
    report_url = db.Column(db.Text,default=None, nullable=True)
    added_by = db.Column(db.Integer, default=0, nullable=True)
    overall_interviewer_video_report=db.Column(db.Text,default=None)
    overall_candidate_video_report=db.Column(db.Text,default=None)
    overall_interviewer_text_report=db.Column(db.Text,default=None)
    overall_candidate_text_report=db.Column(db.Text,default=None)
    overall_interviewer_audio_report=db.Column(db.Text,default=None)
    overall_candidate_audio_report=db.Column(db.Text,default=None)
    video_analysis_status=db.Column(db.String(64),nullable=False,default='pending')
    source_id=db.Column(db.Integer,default=None,nullable=True)
    mobile=db.Column(db.VARCHAR(150),default=None,nullable=True)
    email=db.Column(db.VARCHAR(130),default=None,nullable=False)
    skills=db.Column(db.Text,default=None,nullable=False)
    experience=db.Column(db.VARCHAR(20),default=None,nullable=True)
    datetime=db.Column(db.DateTime,default=None,nullable=False)
    file=db.Column(db.VARCHAR(100),default=None,nullable=False)
    descriptions=db.Column(db.Text,default=None,nullable=False)
    
    def __str__(self):
        return str(self.name)

    def __init__(self, name,source_id,mobile,email,skills,experience,datetime,file,descriptions,interview_video=None,interview_audio=None,is_report_generated=False,report_url=None,added_by=0,overall_interviewer_video_report=None,overall_candidate_video_report=None,overall_interviewer_text_report=None,overall_candidate_text_report=None,overall_interviewer_audio_report=None,overall_candidate_audio_report=None,video_analysis_status='pending'):
        self.name = name
        self.interview_video = interview_video
        self.interview_audio = interview_audio
        self.is_report_generated = is_report_generated
        self.report_url = report_url
        self.added_by = added_by
        self.overall_interviewer_video_report = overall_interviewer_video_report
        self.overall_candidate_video_report = overall_candidate_video_report
        self.overall_interviewer_text_report = overall_interviewer_text_report
        self.overall_candidate_text_report = overall_candidate_text_report
        self.overall_interviewer_audio_report = overall_interviewer_audio_report
        self.overall_candidate_audio_report = overall_candidate_audio_report
        self.video_analysis_status = video_analysis_status
        self.source_id = source_id
        self.mobile=mobile
        self.email=email
        self.skills=skills
        self.experience=experience
        self.datetime=datetime
        self.file=file
        self.descriptions=descriptions

    def user_data(self):
        user = User.query.get(self.added_by)
        if user:
            return user
        else:
            return None

    def get_video_data(id):
        video = Candidate.query.get(id)
        if video:
            return video
        else:
            return None