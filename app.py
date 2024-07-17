from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_posts():
    """Load posts from a JSON file."""
    try:
        with open('posts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_posts(posts):
    """Save posts to a JSON file."""
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=2)


@app.route('/')
def home():
    """
    Render the home page with a list of posts.
    """
    posts = load_posts()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    """
    Render the add post form and handle form submission.
    """
    if request.method == 'POST':
        # Create a new post from the form data.
        new_post = {
            'title': request.form['title'],
            'author': request.form['author'],
            'content': request.form['content']
        }
        # Load existing posts, add the new post, and save the updated list.
        posts = load_posts()
        posts.append(new_post)
        save_posts(posts)
        # Redirect to the home page.
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == '__main__':
    # Run the Flask development server.
    app.run(debug=True)
