from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
def create_default_user():
    # Check if the default user exists
    if not User.query.filter_by(username='demo').first():
        # Create the default user with a hashed password
        hashed_password = generate_password_hash('demo')
        default_user = User(username='demo', password=hashed_password)
        db.session.add(default_user)
        db.session.commit()
        print("Default user created successfully.")




