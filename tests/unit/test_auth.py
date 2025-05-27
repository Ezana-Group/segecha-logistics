import pytest
from app import create_app
from database import db, User

def test_user_creation(session):
    """Test user creation."""
    user = User(
        email='test@example.com',
        password='password123',
        is_admin=False
    )
    session.add(user)
    session.commit()
    
    assert user.id is not None
    assert user.email == 'test@example.com'
    assert user.is_admin is False

def test_user_password_hashing(session):
    """Test password hashing."""
    user = User(
        email='test2@example.com',
        password='password123',
        is_admin=False
    )
    session.add(user)
    session.commit()
    
    assert user.password != 'password123'
    assert user.check_password('password123')
    assert not user.check_password('wrongpassword') 