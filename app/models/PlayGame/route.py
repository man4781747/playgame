from flask import Flask
from flask import render_template
import json
import os
from flask_socketio import SocketIO, emit


global GameStatus
global BaseData
global BaseDataKeyList
BaseData = {}
BaseDataKeyList = []
ChosedList = []
GameStatus = "START"
NowTeamA = ''
NowTeamB = ''


# def loadDataJson():
#     S_FilePath = os.path.join(os.path.split(os.path.realpath(__file__))[0] ,'baseData.json')
#     with open(S_FilePath, 'r', newline='') as jsonfile:
#         BaseData = json.load(jsonfile)
#         for i in range(100):
#             BaseData["test_{}".format(i)] = {
#                 "name": "test_{}".format(i),
#                 "MainPic": "",
#                 "TargetPic": "",
#                 "DesList": [],
#                 "TrueFalse": [],
#                 "Group": i%8
#             }


#         BaseDataKeyList = list(BaseData.keys())
#         print(BaseData)
#         print(BaseDataKeyList)
# loadDataJson()

def home():
    return render_template('main.html')

def GetDataList():
    test = BaseData
    # S_FilePath = os.path.join(os.path.split(os.path.realpath(__file__))[0] ,'baseData.json')
    # with open(S_FilePath, 'r', newline='') as jsonfile:
    #     data = json.load(jsonfile)
    #     # 或者這樣
    #     # data = json.loads(jsonfile.read())
    #     print(data)
    return json.dumps(test)

def GetNowInfo():
    global GameStatus
    return json.dumps({
        'GameStatus': GameStatus,
        'NowPeople': "",
    })

def SetGameStatusRun():
    global GameStatus
    GameStatus = "RUN"
    emit('server_response', {'data': '123'}, broadcast=True, include_self=True)
    return json.dumps({"data":GameStatus})

def SetGameStatusStart():
    global GameStatus
    GameStatus = "START"
    return json.dumps({"data":GameStatus})
