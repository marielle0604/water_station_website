#!/usr/bin/env python3
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app import User, WaterStation

def init_db():
    """Initialize the database"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Tables created successfully!")
        
        # Insert water stations
        stations = [
            "VIOLY'S WATER REFILLING STATION",
            "BWM'S WATER REFILLING STATION", 
            "FERNANDO'S WATER REFILLING STATION",
            "YAKAP AT HALIK WATER REFILLING STATION",
            "MARKEN MIST WATER REFILLING STATION"
        ]
        
        for station in stations:
            if not WaterStation.query.filter_by(name=station).first():
                db.session.add(WaterStation(name=station))
                print(f"✅ Added station: {station}")
        
        # Create default admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@aquavoice.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✅ Default admin created - username: admin, password: admin123")
            print("⚠️  IMPORTANT: Change this password after first login!")
        
        db.session.commit()
        print("🎉 Database initialization complete!")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'init_db':
        init_db()
    else:
        print("Usage: python3 manage.py init_db")
