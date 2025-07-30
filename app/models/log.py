from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


class LogEntry(db.Model):
    """
    Represents a log entry in the database.
    """
    __tablename__ = 'log_entries'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    details = db.Column(JSON, nullable=True)
    operation = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return (f"<LogEntry {self.id}: {self.level} - {self.message} "
                f"at {self.created_at.isoformat()}>")
