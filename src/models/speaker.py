from src.database import db

class Speaker(db.Model):
    __tablename__ = 'speaker'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    user = db.relationship('User', backref=db.backref('speakers', lazy=True, cascade='all,delete'), lazy=False)

    def __repr__(self):
        return '<Speaker %r>' % self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
