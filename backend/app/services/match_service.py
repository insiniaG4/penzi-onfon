from app.models import Match
from app.extensions import db

class MatchService:
    @staticmethod
    def create_match(user_id, matched_user_id):
        new_match = Match(user_id=user_id, matched_user_id=matched_user_id)
        db.session.add(new_match)
        db.session.commit()
        return new_match

    @staticmethod
    def get_matches(user_id):
        return Match.query.filter((Match.user_id == user_id) | (Match.matched_user_id == user_id)).all()