from email import message
from flask import render_template, url_for, redirect, request, flash
from blog import app, db
from blog.models import User, Post, Comment
from blog.forms import RegistrationForm, LoginForm, SortForm, AddCommentForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")

@app.route("/home", methods = ['GET', 'POST'])
def home():
    form = SortForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        if form.date_order.data == 'date_asc':
            posts = Post.query.order_by(Post.date.asc()).all()
        else:
            posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('home.html', posts = posts, form = form)

@app.route("/post/<int:post_id>", methods = ["GET", "POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id = post.id).all()
    form = AddCommentForm()
    if form.validate_on_submit():
        comment = Comment(rating = form.rating.data, content = form.comment.data, post_id = post.id, visitor_id = current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added to the post', 'success')
        return redirect(request.url)
    return render_template('post.html', title = post.title, post = post, comments = comments, form = form)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name = form.first_name.data, email = form.email.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('You\'ve successfully registered and logged in,' + ' ' + current_user.first_name + '!')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('You\'ve successfully logged in,' + ' ' + current_user.first_name + '!')
            return redirect(url_for('home'))
        return render_template('login_error.html')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))
