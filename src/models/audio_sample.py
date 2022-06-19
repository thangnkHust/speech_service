from src.database import db

class AudioSample(db.Model):
    __tablename__ = 'audio_sample'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    path = db.Column(db.String(300), unique=True, nullable=False)
    feature_data = db.Column(db.LargeBinary, nullable=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speaker.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    speaker = db.relationship('Speaker', backref=db.backref('audio_samples', lazy=True, cascade='all,delete'), lazy=False)

    def __repr__(self):
        return '<AudioSample %r>' % self.path

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path
        }
