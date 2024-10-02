from flask import render_template, url_for, flash, redirect
from flaskApp import app, db, bcrypt
from flaskApp.models import User, Blog
from flaskApp.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

blogs = [
    {
        'author': 'John Doe',
        'title': 'Blog Post 1',
        'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. At nam modi tempora placeat ipsa, magni porro voluptatem quos optio. Delectus amet nam corporis placeat aliquam. Voluptatum ab beatae amet qui.',
        'date_posted': 'October 1 2024'
    },
    {
        'author': 'Jane McDoe',
        'title': 'Blog Post 2',
        'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam dicta nihil atque unde, praesentium adipisci a optio aut vero totam, magni provident sit? Sit tenetur mollitia consequatur sequi esse. Eos.',
        'date_posted': 'September 30 2024'
    }
]

@app.route("/")
@app.route("/home")
def home():
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

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')