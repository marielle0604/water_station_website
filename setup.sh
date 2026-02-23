#!/bin/bash

echo "🔧 Setting up AquaVoice Feedback System..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
pip install --upgrade pip
pip install flask flask-sqlalchemy psycopg2-binary python-dotenv

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << ENVEOF
DATABASE_URL=postgresql://aquavoice_user:your_password@localhost:5432/aquavoice_db
SECRET_KEY=your-secret-key-here-change-this
ENVEOF
fi

# Create init_db.py if it doesn't exist
if [ ! -f init_db.py ]; then
    echo "📝 Creating database initialization script..."
    cat > init_db.py << PYEOF
#!/usr/bin/env python3
from app import app, db
from app import WaterStation

def init_database():
    with app.app_context():
        db.create_all()
        print("✅ Tables created successfully!")
        
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
        
        db.session.commit()
        print("🎉 Database initialization complete!")

if __name__ == "__main__":
    init_database()
PYEOF
    chmod +x init_db.py
fi

echo ""
echo "⚠️  Please update your .env file with correct database credentials!"
echo "📋 Current .env file content:"
cat .env
echo ""
echo "🚀 To initialize database, run: python3 init_db.py"
echo "🌐 To start the application, run: python3 app.py"
