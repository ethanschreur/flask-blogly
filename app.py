from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag

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
    all_tags = Tag.query.all()
    return render_template('add_post.html', user=user, all_tags=all_tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_form_handle(user_id):
    title = request.form['title']
    content = request.form['content']
    newPost = Post(title = title, content = content, user_id = user_id)
    lst = request.form.getlist('tag')
    for tag_id in lst:
        tag = Tag.query.get(tag_id)
        newPost.tags.append(tag)
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
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags= tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_handle(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    lst = request.form.getlist("tag")
    for tags in post.tags:
        if (tags.id not in lst):
          posttag = PostTag.query.get((post.id, tags.id))
          db.session.delete(posttag)
          db.session.commit()


    for id in lst:
        tag = Tag.query.get(id)
        post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    user_id = Post.query.get(post_id).user.id
    db.session.delete(Post.query.get(post_id))
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/tags')
def list_tags():
    tags_info = Tag.query.all()
    return render_template('list_tags.html', tags_info = tags_info)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('show_tag_info.html', tag = tag)

@app.route('/tags/new', methods=['GET'])
def new_tag():
    return render_template('new_tag_form.html')

@app.route('/tags/new', methods=['POST'])
def add_tag():
    tag_name = request.form['tag_name']
    new_tag = Tag(name = tag_name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag_post(tag_id):
    tag = Tag.query.get(tag_id)
    tag.name = request.form['name']
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['GET','POST'])
def delete_tag(tag_id):
    db.session.delete(Tag.query.get(tag_id))
    db.session.commit()
    return redirect('/tags')


