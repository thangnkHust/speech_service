from src.database import db

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    role_type = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return '<Role %d>' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'role_type': self.role_type
        }
