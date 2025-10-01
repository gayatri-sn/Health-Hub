from controller.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # Relationships
    roles = db.relationship('UserRole', back_populates='user', cascade='all, delete-orphan')
    doctor_profile = db.relationship('Doctor', back_populates='user', uselist=False)
    patient_profile = db.relationship('Patient', back_populates='user', uselist=False)
    admin_profile = db.relationship('Admin', back_populates='user', uselist=False)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # Relationships
    users = db.relationship('UserRole', back_populates='role', cascade='all, delete-orphan')

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='roles')
    role = db.relationship('Role', back_populates='users')

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Relationships
    doctors = db.relationship('Doctor', back_populates='department')
    appointments = db.relationship('Appointment', back_populates='department')

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    profile = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='doctor_profile')
    department = db.relationship('Department', back_populates='doctors')
    appointments = db.relationship('Appointment', back_populates='doctor')
    availabilities = db.relationship('Availability', back_populates='doctor')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='patient_profile')
    appointments = db.relationship('Appointment', back_populates='patient')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Booked')

    # Foreign Keys
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

    # Relationships
    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')
    department = db.relationship('Department', back_populates='appointments')
    treatment = db.relationship('Treatment', back_populates='appointment', uselist=False)


class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=False)

    # Foreign Keys
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False, unique=True)

    # Relationships
    appointment = db.relationship('Appointment', back_populates='treatment')

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Available')

    # Foreign Keys
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    # Relationships
    doctor = db.relationship('Doctor', back_populates='availabilities')

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='admin_profile')