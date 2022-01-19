var Vue_main = new Vue({
	el: '#app',
	data: {
		teamA: 1,
    teamB: 2,
    GameStatus: 'START',
    NowPeopleInfo: {},
    AllDataList : {},
    GameType : 'TargetPic',
    NextBoss: false,
    NowPoepleQuestsList: [],
    NowQuestName: '',
    NextQuestName: '',
	},
  
	computed: {
	},
  
	methods: {
		// getAllDataList(){
    //   fetch('/GetDataList')
    //   .then(function(response) {
    //     return response.json();
    //   })
    //   .then(function(myJson) {
    //     console.log(myJson);
    //   });
		// },

    // getNowPageInfos(){
    //   fetch('/getNowPageInfos')
    //   .then(function(response) {
    //     return response.json();
    //   })
    //   .then(function(myJson) {
    //     console.log(myJson);
    //     return myJson;
    //   })
    //   .then(function(myJson) {
    //     Vue_main.GameStatus = myJson.GameStatus
    //     Vue_main.NowPeopleInfo = myJson.NowPeople
    //     Vue_main.GameType = myJson.GameType
    //     Vue_main.TeamA = myJson.TeamA
    //     Vue_main.teamB = myJson.teamB
    //   });
    // },

    go_next_people(){
      socket.emit('go_next_people', {
        Boss: this.NextBoss,
        NextPeopleName: this.NextQuestName,
      });
    },

    run_game(){
      socket.emit('go_run_game', {
        Boss: this.NextBoss,
        NextPeopleName: this.NextQuestName,
      });
    },

    changeVSGroup(){
      socket.emit('go_change_VS_group', {
        teamA: this.teamA,
        teamB: this.teamB,
      });
    },
    changeGameType(){
      socket.emit('go_change_game_type', {
        GameType: this.GameType
      });
    },
    show_ans(){
        socket.emit('go_show_ans', {
          Test: ''
        });
      },

    reset_quests(){
        socket.emit('reset_quests', {
            Test: ''
        });
        socket.emit('go_change_VS_group', {
            teamA: this.teamA,
            teamB: this.teamB,
        });
    },
      
  },

	mounted: function(){
    // this.getNowPageInfos()
	},
})

// var clock = setInterval(printword , 1000);
// function printword(){
//   console.log("hello");
//   fetch('/GetNowInfo')
//   .then(function(response) {
//     return response.json();
//   })
//   .then(function(myJson) {
//     console.log(myJson);
//     return myJson
//   })
//   .then(function(myJson) {
//     Vue_main.GameStatus = myJson.GameStatus
//     Vue_main.NowPeople = myJson.NowPeople
//   });
// }

var socket;

$(document).ready(function() {
  var url = 'http://34.80.222.210';
  var port = '7788';
  socket = io.connect(url + ':' + port);
  socket.on('connect', function() {
  socket.emit('connect_event', {data: 'connected!'});})

  socket.on('next_people', function(msg) {
      console.log(msg)
      // Vue_main.NowPeopleInfo = msg
  });

  socket.on('run_game', function(msg) {
    Vue_main.GameStatus = 'RUN'
  });

  socket.on('change_VS_group', function(msg) {
    Vue_main.GameStatus = 'START'
    Vue_main.NowPeopleInfo = {}
    Vue_main.teamA = msg.teamA
    Vue_main.teamB = msg.teamB
  });

  socket.on('change_game_type', function(msg) {
    Vue_main.GameType = msg
  });

  socket.on('NowPoepleQuestsList', function(msg) {
    Vue_main.NowPoepleQuestsList = msg
    if (msg.length != 0){
      Vue_main.NextQuestName = msg[0].name
    }
  });
  socket.on('GetNowPeopleInfo', function(msg) {
    Vue_main.NowPeopleInfo = msg
  });

  return false;});