from app import db


class MathRequest(db.Model):
    __tablename__ = 'math_requests'

    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(50), nullable=False)
    input_value = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    processing_time = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return (f"<Request {self.id}: {self.operation}({self.input_value}) "
                f"= {self.result}>")
