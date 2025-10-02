from main import app
from flask import render_template, redirect, session, url_for, request, flash
from controller.database import db
from controller.models import *

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # check if user is already logged in then redirect to dashboard
        if 'user_email' in session:
            return redirect(url_for('home'))
        
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not email or not password:
            flash('Please enter both email and password', 'danger')
            return redirect(url_for('login'))
        
        if '@' not in email:
            flash('Please enter a valid email address', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first() 

        if user and user.password == password:

            session['user_email'] = user.email
            session['user_role'] = [ur.role.name for ur in user.roles]

            # Set session or token here for logged in user
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to a dashboard or home page
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        
@app.route('/logout')
def logout():
    if 'user_email' not in session:
        flash('You are not logged in', 'warning')
        return redirect(url_for('login'))

    session.pop('user_email', None)
    session.pop('user_role', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # check if user is already logged in then redirect to dashboard
        if 'user_email' in session:
            return redirect(url_for('home'))
        
        return render_template('register.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role_name = request.form.get('role')

        # Validate input
        if not email or not password or not confirm_password or not role_name:
            flash('Please fill out all fields', 'danger')
            return redirect(url_for('register'))
        
        if '@' not in email:
            flash('Please enter a valid email address', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return redirect(url_for('login'))

        role = Role.query.filter_by(name=role_name).first()
        if not role:
            flash('Invalid role selected', 'danger')
            return redirect(url_for('register'))

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        user_role = UserRole(user_id=new_user.id, role_id=role.id)
        db.session.add(user_role)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))