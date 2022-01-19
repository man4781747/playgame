var Vue_main = new Vue({
	el: '#app',
	data: {
        message: '開始'
	},
  
	computed: {},
  
	methods: {
        goStart(){
            var yes = confirm('確定要開始抽獎嗎？');
            if (yes){
                socket.emit('go_start', "");
            }
            
        },
        goStop(){
            socket.emit('go_stop', "");
        },
    },

	mounted: function(){
	},
})

var socket;

$(document).ready(function() {
  var url = 'http://34.80.222.210';
  var port = '80';
  socket = io.connect(url + ':' + port);

  socket.on('START', function(msg) {
    Vue_main.message = '停止'
  });
  socket.on('STOP', function(msg) {
    Vue_main.message = '開始'
  });

  return false;});

