from models import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, render_template


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

