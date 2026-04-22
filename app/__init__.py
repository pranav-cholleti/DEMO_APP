import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'vce-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vce_college.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from . import models
        from . import routes
        app.register_blueprint(routes.bp)
        
        db.create_all()
        
        # Seed College Data
        if not models.Department.query.first():
            depts = [
                models.Department(name='Computer Science & Engineering', code='CSE'),
                models.Department(name='Information Technology', code='IT'),
                models.Department(name='Electronics & Communication', code='ECE')
            ]
            students = [
                models.Student(name='John Doe', roll_no='1602-20-733-001', dept='CSE'),
                models.Student(name='Jane Smith', roll_no='1602-20-737-002', dept='IT')
            ]
            db.session.bulk_save_objects(depts)
            db.session.bulk_save_objects(students)
            db.session.commit()

    return app
