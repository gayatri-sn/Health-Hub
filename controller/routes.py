from main import app
from flask import render_template, redirect, session, url_for, request, flash
from controller.database import db
from controller.models import *

@app.route('/')
def home():
    return render_template('home.html')