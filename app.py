from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET'])
def add_user():
    return render_template('users_new.html')

@app.route('/users/new', methods=['POST'])
def post_add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None
    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user(user_id):
    user = User.query.get(user_id)
    return render_template('users_id.html', user= user)

@app.route('/users/<int:user_id>/edit', methods=['GET'])
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('users_id_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_change(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    if user.image_url == "":
        user.image_url = 'https://t4.ftcdn.net/jpg/03/46/93/61/360_F_346936114_RaxE6OQogebgAWTalE1myseY1Hbb5qPM.jpg'
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    db.session.delete(User.query.get(user_id))
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def post_form(user_id):
    user = User.query.get(user_id)
    return render_template('add_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_form_handle(user_id):
    title = request.form['title']
    content = request.form['content']
    newPost = Post(title = title, content = content, user_id = user_id)
    db.session.add(newPost)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('show_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_handle(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    user_id = Post.query.get(post_id).user.id
    db.session.delete(Post.query.get(post_id))
    db.session.commit()
    return redirect(f'/users/{user_id}')