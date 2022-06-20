from datetime import datetime,timezone,timedelta
from flask_blog import db, login_manager
from flask_login import UserMixin

# Reloading the user from the user ID stored in the session 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    goals = db.relationship('Goal', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object = db.Column(db.String(100), nullable=False)
    key_result = db.Column(db.String(50), nullable=False)
    key_result2 = db.Column(db.String(50), nullable=True)
    key_result3 = db.Column(db.String(50), nullable=True)
    amount = db.Column(db.String(15), nullable=False)
    amount2 = db.Column(db.String(15), nullable=True)
    amount3 = db.Column(db.String(15), nullable=True)
    progress = db.Column(db.String(10), default="0")
    progress2 = db.Column(db.String(10), default="0")
    progress3 = db.Column(db.String(10), default="0")
    note = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    final_score = db.Column(db.Integer, default=0)
    state = db.Column(db.String(10), default="progressing")
    self_review = db.Column(db.Text, nullable=True)

    mon = db.Column(db.String(10), nullable=True, default=0)
    tue = db.Column(db.String(10), nullable=True, default=0)
    wed = db.Column(db.String(10), nullable=True, default=0)
    thu = db.Column(db.String(10), nullable=True, default=0)
    fri = db.Column(db.String(10), nullable=True, default=0)
    sat = db.Column(db.String(10), nullable=True, default=0)
    sun = db.Column(db.String(10), nullable=True, default=0)

    mon2 = db.Column(db.String(10), nullable=True, default=0)
    tue2 = db.Column(db.String(10), nullable=True, default=0)
    wed2 = db.Column(db.String(10), nullable=True, default=0)
    thu2 = db.Column(db.String(10), nullable=True, default=0)
    fri2 = db.Column(db.String(10), nullable=True, default=0)
    sat2 = db.Column(db.String(10), nullable=True, default=0)
    sun2 = db.Column(db.String(10), nullable=True, default=0)

    mon3 = db.Column(db.String(10), nullable=True, default=0)
    tue3 = db.Column(db.String(10), nullable=True, default=0)
    wed3 = db.Column(db.String(10), nullable=True, default=0)
    thu3 = db.Column(db.String(10), nullable=True, default=0)
    fri3 = db.Column(db.String(10), nullable=True, default=0)
    sat3 = db.Column(db.String(10), nullable=True, default=0)
    sun3 = db.Column(db.String(10), nullable=True, default=0)
    
    def __repr__(self):
        return f"Goal('{self.object}', '{self.date_posted}')"
