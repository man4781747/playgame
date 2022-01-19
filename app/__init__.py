from flask import Flask
from app.models.PlayGame import *




def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['SECRET_KEY'] = 'thisisabookandimsupersmart123456'

    PlayGame_app(app)

    return app

