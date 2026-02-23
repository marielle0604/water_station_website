# Flask Project

A Flask web application.

## Setup

1. Create virtual environment: `python3 -m venv venv`
2. Activate environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python app.py`

# Description
- A comprehensive customer feedback management system for water refilling stations built with Flask and PostgreSQL. This application allows customers to submit feedback and provides administrators with a dashboard to manage and analyze responses.

# Features
Customer Portal:
- Feedback Form: Easy-to-use form for customers to submit feedback

- Station Selection: Choose from multiple water refilling stations

- Rating System: 5-star rating interface for quick feedback

- Contact Information: Optional email and phone number collection

- Suggestions Box: Area for customers to provide improvement ideas

- Mobile Responsive: Fully optimized for all device sizes

Admin Dashboard
- Secure Login: Protected admin access with authentication

- Dashboard Overview: Real-time statistics and metrics

- Feedback Management: View, filter, and manage customer feedback

- Status Tracking: Mark feedback as new, read, or archived

- User Management: Create and manage admin users

- Station Performance: Analytics per water station

- Data Export: View feedback with timestamps and details

# TechStack
- Backend: Python Flask
- Database: PostgreSQL
- Frontend: HTML5, Tailwind CSS, JavaScript
- Authentication: Flask-Login, Flask-Bcrypt

# Prerequisites
- Python 3.11 or higher
- PostgreSQL
- pip (Python package manager) 
- Git

# Installation
1. Clone the repository
- git clone https://github.com/marielle0604/water_station_website
- cd water-station
2. Create and activate virtual environment
- python -m venv venv
- source venv/bin/activate
3. Install dependencies
- pip install -r requirements.txt
4. Initialize the database
- python init_db.py
5. Run the application
- python app.py

# Deployed URL
- Railway : https://water-station-website-production-9018.up.railway.app/