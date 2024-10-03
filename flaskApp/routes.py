import os
from PIL import Image
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flaskApp import app, db, bcrypt
from flaskApp.models import User, Blog
from flaskApp.forms import RegistrationForm, LoginForm, UpdateAccountForm, BlogForm
from flask_login import login_user, current_user, logout_user, login_required

# blogs = [
#     {
#         'author': 'John Doe',
#         'title': 'Blog Post 1',
#         'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. At nam modi tempora placeat ipsa, magni porro voluptatem quos optio. Delectus amet nam corporis placeat aliquam. Voluptatum ab beatae amet qui.',
#         'date_posted': 'October 1 2024'
#     },
#     {
#         'author': 'Jane McDoe',
#         'title': 'Blog Post 2',
#         'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam dicta nihil atque unde, praesentium adipisci a optio aut vero totam, magni provident sit? Sit tenetur mollitia consequatur sequi esse. Eos.',
#         'date_posted': 'September 30 2024'
#     }
# ]

@app.route("/")
@app.route("/home")
def home():
    blogs = Blog.query.all()
    return render_template('home.html', blogs=blogs)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_profile_pic(form_profile_photo):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_profile_photo.filename)
    profile_photo_fn = random_hex + f_ext
    profile_photo_path = os.path.join(app.root_path, 'static/profile_pics', profile_photo_fn)
    
    output_size = (125, 125)
    i = Image.open(form_profile_photo)
    i.thumbnail(output_size)
    
    i.save(profile_photo_path)

    return profile_photo_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_photo.data:
            profile_photo_file = save_profile_pic(form.profile_photo.data)
            current_user.image_file = profile_photo_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been Updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/blog/new", methods=['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(blog)
        db.session.commit()
        flash('Your blog has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_blog.html',
                           title='New Blog',
                           form=form,
                           legend='New Blog')

@app.route("/blog/<int:blog_id>")
def blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return render_template('blog.html', title=blog.title, blog=blog)

@login_required
@app.route("/blog/<int:blog_id>/update", methods=['POST', 'GET'])
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.author != current_user:
        abort(403)
    form = BlogForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
        flash('Your Blog has been Updated', 'success')
        return redirect(url_for('blog', blog_id=blog.id))
    elif request.method == 'GET':
            form.title.data = blog.title
            form.content.data = blog.content
    return render_template('create_blog.html',
                           title='Update Blog',
                           form=form,
                           legend='Update Blog')

@login_required
@app.route("/blog/<int:blog_id>/delete", methods=['POST'])
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.author != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
    flash('Your blog has been deleted', 'success')
    return redirect(url_for('home'))

