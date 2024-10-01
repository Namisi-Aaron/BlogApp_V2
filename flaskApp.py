from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '010f96a8f081c423b728e0eafa7e588a'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root123@localhost:5432/blogapp'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    blogs = db.relationship('Blog', backref='author', lazy=True)

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.username, self.email, self.image_file)
    
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Post('{}', '{}')".format(self.title, self.date_posted)

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Invalid credentials', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)