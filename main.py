from flask import Flask
from flask import render_template
from app import *
from flask_socketio import SocketIO, emit
import json
import os
import random
global GameStatus
GameStatus = "START"
global NowPeopleInfo
NowPeopleInfo = {}
global NowPeopleQuest
NowPeopleQuest = {}
global GameType
GameType = 'TargetPic'
global TeamA, teamB
TeamA = 1
teamB = 2
global AnsList
AnsList = []

global BaseData

def loadDataJson():
    S_FilePath = os.path.join(os.path.split(os.path.realpath(__file__))[0] ,'baseData.json')
    with open(S_FilePath, 'r', newline='') as jsonfile:
        BaseData = json.load(jsonfile)
        # for i in range(100):
        #     BaseData["test_{}".format(i)] = {
        #         "name": "test_{}".format(i),
        #         "MainPic": "/static/pictures/mainPic/Catmain.jpg",
        #         "TargetPic": "/static/pictures/partPic/CatPart.jpg",
        #         "DesList": [
        #             '描述1 - {}'.format(i),
        #             '描述2 - {}'.format(i),
        #             '描述3 - {}'.format(i), 
        #         ],
        #         "TrueFalse": [
        #             ['測試題目1 - {}'.format(i), True],
        #             ['測試題目2 - {}'.format(i), True],
        #             ['測試題目3 - {}'.format(i), True],
        #             ['測試題目4 - {}'.format(i), True],
        #         ],
        #         "Group": i%8,
        #         "Boss": False,
        #     }
        #     randomIndex = random.randint(0,3)
        #     BaseData["test_{}".format(i)]["TrueFalse"][randomIndex][1] = False
    return BaseData
BaseData = loadDataJson()
print(BaseData)

global poepleList
poepleList = []

def ResetAllQuests():
    global BaseData
    L_keyList = []
    for Key in BaseData.keys():
        BaseData[Key]['del'] = False

def GetQuestsList(BaseData, teamA, teamB):
    L_keyList = []
    for Key in BaseData.keys():
        if BaseData[Key]['Group'] not in [int(teamA), int(teamB)]:
            if BaseData[Key].get('del', False) != True:
                L_keyList.append(Key)
            random.shuffle(L_keyList)
    return L_keyList

app = create_app()
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('client_event')
def client_msg(msg):
    print('client_event')
    print(msg)
    emit('server_response', {'data': msg['data']}, broadcast=True, include_self=True)

@socketio.on('connect_event')
def connected_msg(msg):
    global GameStatus
    global NowPeopleInfo
    global NowPeopleQuest
    global GameType
    global TeamA, teamB
    emit('get_base_data', {
        'GameStatus': GameStatus,
        'NowPeople': NowPeopleQuest,
        'GameType' : GameType,
        'TeamA' : TeamA,
        'teamB': teamB,
        'AnsList': AnsList,
    })
    returnNowPoepleQuestsList(msg)
    returnNowPeopleInfo(msg)


def returnNowPeopleInfo(msg):
    global NowPeopleInfo
    emit('GetNowPeopleInfo', NowPeopleInfo)

def returnNowPoepleQuestsList(msg):
    global poepleList
    L_detail_info_list = []
    for key in poepleList:
        L_detail_info_list.append(BaseData[key])

    emit('NowPoepleQuestsList', L_detail_info_list)

@socketio.on('go_next_people')
def NextPeople(msg):
    global poepleList
    global NowPeopleInfo
    global NowPeopleQuest

    # if msg.get('Boss', False) == True:
    #     for index, key in enumerate(poepleList):
    #         print(index,key)
    #         if BaseData[key]["Boss"] == True:
    #             randomIndex = index
    #             break  
    #     else:
    #         randomIndex = random.randint(0,len(poepleList)-1)
    # else:    
    #     randomIndex = random.randint(0,len(poepleList)-1)
    print(msg)
    randomIndex = poepleList.index(msg["NextPeopleName"])

    NowPeopleInfo = BaseData[poepleList[randomIndex]]
    NowPeopleInfo['del'] = True
    poepleList.pop(randomIndex)
    print(len(poepleList))
    NowPeopleQuest = {
        "MainPic": NowPeopleInfo["MainPic"],
        "TargetPic": NowPeopleInfo["TargetPic"],
        "DesList": NowPeopleInfo["DesList"],
        "TrueFalse": [i[0] for i in NowPeopleInfo["TrueFalse"]],
    }

    global AnsList

    ans_name_list = random.sample(poepleList, 3)
    AnsList = []
    for key in ans_name_list:
        peopleData = BaseData[key]
        AnsList.append(
            {
                'name': peopleData['name'],
                'pic': peopleData['MainPic'],
                'ans': False,
            }
        )
    insertIndex = random.randint(0,3)
    AnsList.insert(insertIndex, {
        'name': NowPeopleInfo['name'],
        'pic': NowPeopleInfo['MainPic'],
        'ans': True,
    })
    print(AnsList)
    emit('next_people', NowPeopleQuest, broadcast=True, include_self=True)
    emit('wrong_ans_peoples', AnsList, broadcast=True, include_self=True)
    returnNowPoepleQuestsList(msg)
    returnNowPeopleInfo(msg)

@socketio.on('go_run_game')
def RunGame(msg):
    global GameStatus
    GameStatus = 'RUN'
    NextPeople(msg)

    emit('run_game', {'data': "test"}, broadcast=True, include_self=True)

@socketio.on('go_change_VS_group')
def go_change_VS_group(msg):
    global poepleList
    global GameStatus
    global NowPeopleInfo
    global TeamA, teamB
    TeamA = msg['teamA']
    teamB = msg['teamB']
    GameStatus = 'START'
    NowPeopleInfo = {}
    poepleList = GetQuestsList(BaseData, TeamA, teamB)
    emit('change_VS_group', msg, broadcast=True, include_self=True)
    returnNowPoepleQuestsList(msg)

@socketio.on('go_change_game_type')
def go_change_game_type(msg):
    global GameType
    GameType = msg['GameType']
    emit('change_game_type', GameType, broadcast=True, include_self=True)

@socketio.on('go_show_ans')
def show_ans(msg):
    global NowPeopleInfo
    global GameType
    for index,q in enumerate(NowPeopleInfo["TrueFalse"]):
        if q[1] == False:
            ansIndex = index
            break
    L_ans = [NowPeopleInfo['name'], ansIndex]
    emit('show_ans', L_ans, broadcast=True, include_self=True)

@socketio.on('reset_quests')
def reset_quests(msg):
    ResetAllQuests()

@app.route("/getNowPageInfos")
def getNowPageInfos():
    global GameStatus
    global NowPeopleInfo
    global GameType
    global TeamA, teamB

    return json.dumps({
        'GameStatus': GameStatus,
        'NowPeople': NowPeopleInfo,
        'GameType' : GameType,
        'TeamA' : TeamA,
        'teamB': teamB,
        'AnsList': AnsList,
    })

@app.route("/adminPage")
def adminPage():
    return render_template('main_admin.html')

#抽獎箱相關
@socketio.on('go_start')
def go_start(msg):
    print("go_start")
    emit('START', "", broadcast=True, include_self=True)

@socketio.on('go_stop')
def go_stop(msg):
    emit('STOP', "", broadcast=True, include_self=True)

@app.route("/lotteryGround")
def lottery_ground():
    return render_template('main_lottery.html')

@app.route("/lotteryGround/admin")
def main_lottery_admin():
    return render_template('main_lottery_admin.html')


if __name__ == '__main__':
    app.debug = True
    socketio.run(app, port=7788, debug=True)