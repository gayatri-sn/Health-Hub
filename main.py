from flask import Flask, render_template
from controller.database import db
from controller.config import Config
from controller.models import *

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin')
        db.session.add(admin_role)

    
    doctor_role = Role.query.filter_by(name='doctor').first()
    if not doctor_role:
        doctor_role = Role(name='doctor')
        db.session.add(doctor_role)

    patient_role = Role.query.filter_by(name='patient').first()
    if not patient_role:
        patient_role = Role(name='patient')
        db.session.add(patient_role)

    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

# hi