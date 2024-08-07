from flask import Flask, render_template, request, redirect, url_for
import json
import uuid
import os

app = Flask(__name__)


def load_posts():
    """Load posts from a JSON file."""
    try:
        with open('posts.json', 'r') as f:
            posts = json.load(f)
            for post in posts:
                if 'likes' not in post:
                    post['likes'] = 0
            return posts
    except FileNotFoundError:
        return []


def save_posts(posts):
    """Save posts to a JSON file."""
    with open('posts.json', 'w') as f:
        json.dump(posts, f, indent=2)


def fetch_post_by_id(post_id):
    """Fetch a single post by its ID."""
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def home():
    """Render the home page with a list of posts."""
    posts = load_posts()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    """Render the add post form and handle form submission."""
    if request.method == 'POST':
        # Create a new post from the form data.
        new_post = {
            'id': str(uuid.uuid4()),  # Generate a unique ID for the new post.
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'content': request.form.get('content'),
            'likes': 0  # Initialize likes to 0
        }
        # Load existing posts, add the new post, and save the updated list.
        posts = load_posts()
        posts.append(new_post)
        save_posts(posts)
        # Redirect to the home page.
        return redirect(url_for('home'))
    # Render the add post form.
    return render_template('add.html')


@app.route('/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
    """Delete the specified blog post and redirect to the home page."""
    posts = load_posts()
    posts = [post for post in posts if post['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('home'))


@app.route('/update/<post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    """Update the specified blog post."""
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['author'] = request.form['author']
        post['content'] = request.form['content']

        posts = load_posts()
        for i, p in enumerate(posts):
            if p['id'] == post_id:
                posts[i] = post
                break
        save_posts(posts)
        return redirect(url_for('home'))

    return render_template('update.html', post=post)


@app.route('/like/<post_id>', methods=['POST'])
def like_post(post_id):
    """Increment the likes of the specified blog post."""
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            post['likes'] += 1
            break
    save_posts(posts)
    return redirect(url_for('home'))


if __name__ == '__main__':
    # Run the Flask development server.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=5000)
