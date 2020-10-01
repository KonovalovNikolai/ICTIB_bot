from flask import Flask
from config import TOKEN

app = Flask(__name__)
app.config['SECRET_KEY'] = TOKEN

from app import routes