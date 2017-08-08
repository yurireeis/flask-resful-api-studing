from app import app
from db import db

db.init_app(app)


# using flask decorator to create database and schema if not exists
@app.before_first_request
def create_tables():
    db.create_all()
