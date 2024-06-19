from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NoAdmissions(db.Model):
    facId = db.Column(db.String(50), nullable=False)
    patientId = db.Column(db.String(50), nullable=False, unique=True, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    birthDate = db.Column(db.Date)
    admissionDate = db.Column(db.DateTime, nullable=False)
