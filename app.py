from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
#  app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.secret_key = "dev-secret"

# Blog setup
BLOG_FILE = Path('data/blog_posts.json')
Path('data').mkdir(exist_ok=True)

def get_blog_posts():
    if not BLOG_FILE.exists():
        with open(BLOG_FILE, 'w') as f:
            json.dump([], f)
        return []
    
    try:
        with open(BLOG_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(BLOG_FILE, 'w') as f:
            json.dump([], f)
        return []

def save_blog_post(title, content):
    posts = get_blog_posts()
    posts.append({
        'id': len(posts) + 1,
        'title': title,
        'content': content,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    with open(BLOG_FILE, 'w') as f:
        json.dump(posts, f, indent=2)

# CI/CD status reader
def get_ci_status():
    try:
        with open('data/ci_status.json') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "status": "unknown",
            "timestamp": "N/A",
            "message": "No CI/CD info available"
        }

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    ci_status = get_ci_status()
    return render_template('dashboard.html', ci_status=ci_status)

@app.route('/blog')
def blog():
    return render_template('blog.html', posts=get_blog_posts())

@app.route('/write-blog', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            save_blog_post(title, content)
            flash('Blog post published!', 'success')
            return redirect(url_for('blog'))
        flash('Title and content required!', 'error')
    return render_template('write_blog.html')

@app.route('/delete-blog/<int:post_id>', methods=['POST'])
def delete_blog(post_id):
    posts = get_blog_posts()
    posts = [post for post in posts if post['id'] != post_id]
    with open(BLOG_FILE, 'w') as f:
        json.dump(posts, f, indent=2)
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('blog'))

if __name__ == '__main__':
    app.run(debug=True)
