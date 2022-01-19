from flask import Flask
from . import route
import os

def PlayGame_app(flask_app):
    flask_app.add_url_rule('/', 
        'PlayGame', route.home, methods=['GET']
    )

    flask_app.add_url_rule('/GetDataList', 
        'GetDataList', route.GetDataList, methods=['GET']
    )

    flask_app.add_url_rule('/SetGameStatusRun', 
        'SetGameStatusRun', route.SetGameStatusRun, methods=['GET']
    )

    flask_app.add_url_rule('/SetGameStatusStart', 
        'SetGameStatusStart', route.SetGameStatusStart, methods=['GET']
    )

    flask_app.add_url_rule('/GetNowInfo', 
        'GetNowInfo', route.GetNowInfo, methods=['GET']
    )

    return flask_app