from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    news_posts = db.relationship('News', backref='author', lazy='dynamic')
    marketplace_items = db.relationship('MarketplaceItem', backref='seller', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    category = db.Column(db.String(50))  # camera, mobile, car
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_url = db.Column(db.String(200))

class MarketplaceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))  # camera, mobile, car
    condition = db.Column(db.String(50))  # new, used
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    images = db.relationship('ItemImage', backref='item', lazy='dynamic')

class ItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('marketplace_item.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)