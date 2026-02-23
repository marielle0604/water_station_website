#!/usr/bin/env python3
from app import app, db
from app import User, WaterStation
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

def init_auth():
    with app.app_context():
        # Create tables
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
            admin.set_password('admin123')  # Change this!
            db.session.add(admin)
            print("✅ Default admin created - username: admin, password: admin123")
            print("⚠️  IMPORTANT: Change this password after first login!")
        
        db.session.commit()
        print("🎉 Authentication system initialized successfully!")

if __name__ == "__main__":
    init_auth()