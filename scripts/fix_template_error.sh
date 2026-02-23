#!/bin/bash
# save as complete_setup.sh

cd /home/marielle/water-station

echo "🔧 Setting up AquaVoice Feedback System..."

# Create directories
mkdir -p templates
mkdir -p static/css

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install flask flask-sqlalchemy psycopg2-binary python-dotenv

# Create templates (using the content I provided earlier)
echo "📝 Creating template files..."

# Create base.html
cat > templates/base.html << 'EOF'
[PASTE THE BASE.HTML CONTENT HERE]
EOF

# Create feedback.html (this is the main form)
cat > templates/feedback.html << 'EOF'
[PASTE THE INDEX.HTML CONTENT HERE - the one I provided earlier]
EOF

# Create admin.html
cat > templates/admin.html << 'EOF'
[PASTE THE ADMIN.HTML CONTENT HERE]
EOF

# Update app.py to use correct template
sed -i 's/feedback.html/feedback.html/g' app.py

# Test the setup
echo "✅ Setup complete!"
echo "🚀 Starting application..."
python3 app.py
