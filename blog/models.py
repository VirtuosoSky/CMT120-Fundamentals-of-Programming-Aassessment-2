from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    title = db.Column(db.Text, nullable = False)
    short_description = db.Column(db.Text, nullable = False)
    detailed_description = db.Column(db.Text, nullable = False)
    image_file = db.Column(db.String(40), nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    comments = db.relationship('Comment', backref='post', lazy = True)

    def get_comments(self):
        return Comment.query.filter_by(post_id = Post.id).order_by(Comment.date.desc())

    def __repr__(self):
        return f"Post('{self.date}', '{self.title}', '{self.content}', '{self.comments}')"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(20))
    email = db.Column(db.String(20), unique = True, nullable = False)
    hashed_password = db.Column(db.String(128))
    post = db.relationship('Post', backref = 'user', lazy = True)
    comments = db.relationship('Comment', backref = 'visitor', lazy = True)
    
    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}', '{self.password}')"
    
    @property
    def password(self):
        raise AttributeError('Password is not readable.')
    
    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    content = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    def __repr__(self):
        return f"Comment('{self.visitor_id}', '{self.timestamp}', '{self.content}', '{self.rating}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))