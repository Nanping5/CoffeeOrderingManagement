#!/usr/bin/env python3
"""
Initialize SQLite database for testing
"""
import os
import sys
from datetime import datetime

# Add the backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set SQLite environment variable before importing app
os.environ['DATABASE_URL'] = 'sqlite:///coffee_ordering.db'
os.environ['FLASK_ENV'] = 'development'

from app import create_app
from extensions import db
from models.user import User
from models.menu import MenuItem
from models.order import Order
from models.order_item import OrderItem

def init_database():
    """Initialize database with tables and sample data"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        
        # Create demo users
        print("Creating demo users...")
        
        # Admin user
        admin = User(
            username='admin',
            email='admin@coffee.com',
            password='admin123',
            role='admin'
        )
        
        # Test user
        testuser = User(
            username='testuser',
            email='test@coffee.com',
            password='admin123',
            role='user'
        )
        
        db.session.add(admin)
        db.session.add(testuser)
        
        # Create sample menu items
        print("Creating sample menu items...")
        menu_items = [
            MenuItem(
                name='Espresso',
                price=3.50,
                description='Strong and bold Italian coffee',
                category='Hot Coffee',
                image_url='/images/espresso.jpg',
                is_available=True
            ),
            MenuItem(
                name='Cappuccino',
                price=4.50,
                description='Espresso with steamed milk foam',
                category='Hot Coffee',
                image_url='/images/cappuccino.jpg',
                is_available=True
            ),
            MenuItem(
                name='Latte',
                price=4.00,
                description='Smooth espresso with steamed milk',
                category='Hot Coffee',
                image_url='/images/latte.jpg',
                is_available=True
            ),
            MenuItem(
                name='Iced Coffee',
                price=3.75,
                description='Refreshing cold brewed coffee',
                category='Cold Coffee',
                image_url='/images/iced-coffee.jpg',
                is_available=True
            ),
            MenuItem(
                name='Croissant',
                price=2.50,
                description='Buttery French pastry',
                category='Pastries',
                image_url='/images/croissant.jpg',
                is_available=True
            )
        ]
        
        for item in menu_items:
            db.session.add(item)
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "="*50)
        print("Database initialized successfully!")
        print("="*50)
        print(f"\nDemo Users:")
        print(f"  Admin: username='admin', password='admin123'")
        print(f"  User:  username='testuser', password='admin123'")
        print(f"\nMenu Items: {len(menu_items)} items created")
        print(f"\nDatabase: coffee_ordering.db")
        print("="*50)

if __name__ == '__main__':
    init_database()
