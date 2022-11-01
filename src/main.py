from flask import Flask
from db import db, ma

app = Flask(__name__)

@app.route('/')
def home():
    return 'hello world'
