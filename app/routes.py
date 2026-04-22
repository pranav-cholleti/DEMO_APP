from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models import Department, Student, db
from sqlalchemy import text
import os

bp = Blueprint('vce', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/departments')
def departments():
    depts = Department.query.all()
    return render_template('departments.html', depts=depts)

@bp.route('/placements')
def placements():
    """
    INTENTIONAL BUG: Routing Issue. 
    User wants this to point to placements page, but it renders departments.
    """
    depts = Department.query.all()
    return render_template('departments.html', depts=depts)

@bp.route('/search')
def search():
    """
    VULNERABILITY: SQL Injection (CWE-89)
    """
    query = request.args.get('q', '')
    if query:
        # Dangerous raw SQL concatenation
        sql = f"SELECT * FROM student WHERE name LIKE '%{query}%'"
        results = db.session.execute(text(sql)).fetchall()
        return render_template('search.html', results=results, query=query)
    return render_template('search.html', results=[], query='')

@bp.route('/admin/db-reset', methods=['GET', 'POST'])
def db_reset():
    """
    VULNERABILITY: Broken Access Control (CWE-284)
    No authentication required to reset the database.
    """
    db.drop_all()
    db.create_all()
    return "Database has been reset successfully!", 200

@bp.route('/config/env')
def show_env():
    """
    VULNERABILITY: Information Exposure (CWE-200)
    """
    return jsonify(dict(os.environ))
