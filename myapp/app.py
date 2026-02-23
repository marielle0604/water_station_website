import os
import traceback
from myapp.utils import init_db
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-12345')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://aquavoice_user:your_password@localhost:5432/aquavoice_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Admin required decorator - ONLY ONE INSTANCE
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('index'))  # ← CHANGED TO index (NOT admin)
        return f(*args, **kwargs)
    return decorated_function

# Database Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    stations = WaterStation.query.all()
    return render_template('index.html', stations=stations)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('register'))
        
        # Check if user exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            print(f"Registration error: {str(e)}")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.form.get('ajax') == 'true':
            return jsonify({
                'success': True,
                'message': 'Already logged in',
                'redirect': url_for('admin')
            })
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.form.get('ajax') == 'true'
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            if is_ajax:
                # Return JSON response for AJAX requests
                return jsonify({
                    'success': True,
                    'message': f'Welcome back, {user.username}!',
                    'redirect': url_for('admin')
                })
            
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin'))
        else:
            if is_ajax:
                # Return JSON response for AJAX requests
                return jsonify({
                    'success': False,
                    'message': 'Invalid username or password.'
                }), 401
            
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

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
        db.session.rollback()
        print(f"Error submitting feedback: {str(e)}")
        flash('Error submitting feedback. Please try again.', 'danger')
        return redirect(url_for('index'))

@app.route('/admin')
@login_required
@admin_required
def admin():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    stations = WaterStation.query.all()
    users = User.query.all()
    
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
                         users=users,
                         total_feedbacks=total_feedbacks,
                         avg_rating=round(avg_rating, 1),
                         station_stats=station_stats)

@app.route('/admin/update-status/<int:feedback_id>', methods=['POST'])
@login_required
@admin_required
def update_status(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    new_status = request.json.get('status')
    if new_status in ['new', 'read', 'archived']:
        feedback.status = new_status
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@app.route('/admin/delete/<int:feedback_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/admin/user/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id != current_user.id:  # Can't change your own admin status
        user.is_admin = not user.is_admin
        db.session.commit()
        return jsonify({'success': True, 'is_admin': user.is_admin})
    return jsonify({'success': False, 'message': 'Cannot modify your own admin status'}), 400

@app.route('/admin/user/<int:user_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id != current_user.id:  # Can't delete yourself
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Cannot delete your own account'}), 400

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
        
        # Create default admin if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@aquavoice.com',
                is_admin=True
            )
            admin.set_password('admin123')  # Change this in production!
            db.session.add(admin)
            print("Default admin created - username: admin, password: admin123")
        
        db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000)