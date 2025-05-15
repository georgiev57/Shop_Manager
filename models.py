from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transactions'  # optional, for clarity
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
