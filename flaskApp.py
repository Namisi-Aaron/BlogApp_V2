from flask import Flask, render_template, url_for

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)