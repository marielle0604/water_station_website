import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-12345')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/aquavoice_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class WaterStation(db.Model):
    __tablename__ = 'water_stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    feedbacks = db.relationship('Feedback', backref='station', lazy=True)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('water_stations.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    rating = db.Column(db.Integer, nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    suggestions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='new')

# Routes
@app.route('/')
def index():
    stations = WaterStation.query.all()
    return render_template('index.html', stations=stations)

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        feedback = Feedback(
            station_id=request.form['station'],
            customer_name=request.form['customer_name'],
            email=request.form.get('email', ''),
            phone=request.form.get('phone', ''),
            rating=int(request.form['rating']),
            feedback_text=request.form['feedback'],
            suggestions=request.form.get('suggestions', '')
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash('Error submitting feedback. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/admin')
def admin():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    stations = WaterStation.query.all()
    
    # Calculate statistics
    total_feedbacks = len(feedbacks)
    avg_rating = db.session.query(db.func.avg(Feedback.rating)).scalar() or 0
    
    # Feedback by station
    station_stats = []
    for station in stations:
        count = Feedback.query.filter_by(station_id=station.id).count()
        avg = db.session.query(db.func.avg(Feedback.rating)).filter(Feedback.station_id == station.id).scalar() or 0
        station_stats.append({
            'name': station.name,
            'count': count,
            'avg_rating': round(avg, 1)
        })
    
    return render_template('admin.html', 
                         feedbacks=feedbacks, 
                         total_feedbacks=total_feedbacks,
                         avg_rating=round(avg_rating, 1),
                         station_stats=station_stats)

@app.route('/admin/update-status/<int:feedback_id>', methods=['POST'])
def update_status(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    new_status = request.json.get('status')
    if new_status in ['new', 'read', 'archived']:
        feedback.status = new_status
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@app.route('/admin/delete/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Ensure stations exist
        stations = [
            "VIOLY'S WATER REFILLING STATION",
            "BWM'S WATER REFILLING STATION", 
            "FERNANDO'S WATER REFILLING STATION",
            "YAKAP AT HALIK WATER REFILLING STATION",
            "MARKEN MIST WATER REFILLING STATION"
        ]
        for station_name in stations:
            if not WaterStation.query.filter_by(name=station_name).first():
                db.session.add(WaterStation(name=station_name))
        db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000)