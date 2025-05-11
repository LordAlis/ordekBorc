from datetime import datetime
from .user import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, counter_offer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Counter offer details
    counter_amount = db.Column(db.Float, nullable=True)
    counter_description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Transaction {self.id}: {self.amount} from {self.sender_id} to {self.receiver_id}>'
