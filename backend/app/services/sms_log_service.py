from app.models import SMSLog
from app.extensions import db

class SMSLogService:
    @staticmethod
    def log_sms(from_number, to_number, message_type, message_content):
        new_sms_log = SMSLog(
            from_number=from_number,
            to_number=to_number,
            message_type=message_type,
            message_content=message_content
        )
        db.session.add(new_sms_log)
        db.session.commit()
        return new_sms_log