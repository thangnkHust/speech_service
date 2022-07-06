from nanoid import generate
from src.database import db

class Record(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.String(30), primary_key=True, default=generate())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    record_path = db.Column(db.String(200), nullable=False)
    result_path = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    user = db.relationship('User', backref=db.backref('records', lazy=True, cascade='all,delete'), lazy=False)

    def __repr__(self):
        return '<Record %r>' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.serialize(),
            'record_path': self.record_path,
            'result_path': self.result_path,
            'status': self.status
        }
