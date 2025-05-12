from datetime import datetime
from .user import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    borrower_name = db.Column(db.String(80), nullable=False)  # Name of the person who borrowed
    is_paid = db.Column(db.Boolean, default=False)  # Whether the debt has been paid back
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime, nullable=True)  # When the debt was paid back
    
    # Foreign key for the user who lent the money
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.id}: {self.amount} to {self.borrower_name}>'
