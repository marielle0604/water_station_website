#!/usr/bin/env python3
from app import app, db
from app import WaterStation

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Tables created successfully!")
        
        # Insert stations
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
            else:
                print(f"⏭️  Station already exists: {station}")
        
        db.session.commit()
        print("🎉 Database initialization complete!")

if __name__ == "__main__":
    init_database()
