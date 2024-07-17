import json
from flask import Flask, render_template

app = Flask(__name__)


def load_posts():
    try:
        with open('posts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_posts(posts):
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=2)


@app.route('/')
def home():
    posts = load_posts()
    return render_template('index.html', posts=posts)


# Other routes and functions remain the same...

if __name__ == '__main__':
    app.run(debug=True)
