from datetime import datetime
from . import db

class PriceAlert(db.Model):
    __tablename__ = 'price_alert'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticker = db.Column(db.String(20), nullable=False)
    price_threshold = db.Column(db.Float, nullable=False)
    alert_type = db.Column(db.String(10))  # 'above' or 'below'
    email_enabled = db.Column(db.Boolean, default=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='price_alerts')

    def __repr__(self):
        return f'<PriceAlert {self.ticker} - {self.price_threshold}>'