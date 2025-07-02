from app.extensions import db


class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    matched_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    match_date = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(20), default='pending')

    user = db.relationship('User', foreign_keys=[user_id])
    matched_user = db.relationship('User', foreign_keys=[matched_user_id])

    __table_args__ = (db.UniqueConstraint('user_id', 'matched_user_id'),)

    def __repr__(self):
        return f'<Match {self.id}>'