import pytest
from app import app, db  # Import your Flask app and db

@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create test tables
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after tests

def test_home_page(client):
    """Test the home page returns 200 OK."""
    response = client.get('/')
    assert response.status_code == 200

def test_write_blog_page(client):
    """Test the write-blog page returns 200 OK."""
    response = client.get('/write-blog')
    assert response.status_code == 200

def test_blog_creation(client):
    """Test blog post creation."""
    response = client.post('/write-blog', data={
        'title': 'Test Post',
        'content': 'Test Content'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Post' in response.data
