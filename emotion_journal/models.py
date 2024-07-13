from app import db

class Emotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Emotion {self.emotion}>'
